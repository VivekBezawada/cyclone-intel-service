from datetime import datetime
import os
import sys
import json
import copy
from scraper.utils.transformer import tranform_data_to_tuples_for_insertion, transform_table_to_json, validate_forecast_data
from scraper.utils.html_utils import fetch_cyclones_info_page, fetch_cyclone_details_page

NO_CYCLONES = "No Currently Active Cyclones"
NO_DATA = "No Data Available"


# This first part fetches all the active cyclones
# from the given URL and structures into the requred format
def fetch_active_cyclones():
    cyclone_data = []
    html_body = fetch_cyclones_info_page()
    for html_content in html_body:
        document = {}
        document["region"] = html_content.find("h3").text
        document["forecast_time"] = None
        document["track_data"] = []
        document["forecast_data"] = []
        if html_content.find("ul").find("li").text == NO_CYCLONES:
            continue
        for html_cyclone in html_content.find("ul").findAll("li"):
            cyclone_name = str(html_cyclone.find("a").text).strip()
            document["cyclone_id"] = cyclone_name.split("-")[0].strip()
            document["cyclone_name"] = cyclone_name
            # Identified a bug where a li has 2 elements, it's always taking the latest one
            # Made a deep copy to fix this bug
            cyclone_data.append(copy.deepcopy(document))
    return cyclone_data


# can make it parallel if we want to complete them faster
# Since this is a shceduler, we don"t have any time constraints
# Identified that there are only 3 H3 elements
# Below which either a table exists or not
# Based on that, We can easily identify which table belongs to what
def fetch_details_for_active_cyclones(data):
    for document in data:
        h3_elements = fetch_cyclone_details_page(document["cyclone_id"])
        next_element_for_forecast = h3_elements[0].find_next_sibling()
        next_element_for_track = h3_elements[1].find_next_sibling()
        if str(next_element_for_forecast.text) != NO_DATA:
            # In Forecase, next element is forecast time
            # and next element after that is the table
            # The below substring is what we actually need
            document["forecast_time"] = next_element_for_forecast.text[25:]
            table = next_element_for_forecast.find_next_sibling()
            document["forecast_data"] = transform_table_to_json(document["cyclone_id"],
                                                                table, document["forecast_time"])
            # Validate for empty values. Will not be of help
            # if forecast data has all 0 values
            document["forecast_data"] = validate_forecast_data(
                document["forecast_data"])
        if str(next_element_for_track.text) != NO_DATA:
            document["track_data"] = transform_table_to_json(
                document["cyclone_id"], next_element_for_track)
    return data


def run_scheduler():
    try:
        print("Scheduler triggerred at " + str(datetime.now()))
        cyclone_data = fetch_active_cyclones()
        if (cyclone_data):
            print("Retrieved active cyclones. Fetching track data and forecast data")
            cyclone_data = fetch_details_for_active_cyclones(cyclone_data)
            print("Retrieved track data and forecast data. Transforming and saving to Database")
            return tranform_data_to_tuples_for_insertion(cyclone_data)
        else:
            print("There are no active cyclones at this moment")
        print("Scheduler is completed at " + str(datetime.now()))
        return None
    except Exception as e:
        print("Exception occured while processing " + str(e))
        return None
