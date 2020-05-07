import urllib.request as request
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import psycopg2 as pyc
from psycopg2.extras import execute_values

# TODO : Add readme file to explain on conflict
# SQL Insert queries
INSERT_CYCLONE_INFO    = "INSERT INTO cyclone_info (cyclone_id, cyclone_name, region) VALUES %s ON CONFLICT DO NOTHING"
INSERT_TRACK_DATA      = "INSERT INTO track_data (cyclone_id, synoptic_time, latitude, longitude, intensity) VALUES %s ON CONFLICT DO NOTHING"
INSERT_FORECAST_DATA   = "INSERT INTO forecast_data (cyclone_id, forecast_time, latitude, longitude, intensity) VALUES %s ON CONFLICT DO NOTHING"

#Cyclone info base url
CYCLONE_INFO_URL = "http://rammb.cira.colostate.edu/products/tc_realtime/index.asp"

#Cyclone track history and forecast data
CYCLONE_DETAIL_URL = "https://rammb-data.cira.colostate.edu/tc_realtime/storm.asp?storm_identifier="

DATE_FORMAT = "%Y-%m-%d %H:%M"
NO_CYCLONES = "No Currently Active Cyclones"
NO_DATA = "No Data Available"

def get_cyclone_detail_url(cyclone_id):
    return CYCLONE_DETAIL_URL + cyclone_id

def fetch_timestamp_from_date(date, hours=0):
    date = datetime.strptime(date, DATE_FORMAT) + timedelta(hours=hours)
    return date.timestamp()

def fetch_html_content(url, attrs1, element , attrs2=None):
    page = request.urlopen(url)
    soup = BeautifulSoup(page, features="lxml")
    return soup.body.find("div", attrs=attrs1).findAll(element, attrs=attrs2)

def convert_table_to_json(table, last_forecast_time=None):
    forecast_data = []
    for index,info in enumerate(table.findAll("tr")):
        if index == 0:
            continue
        forecast_document = {}
        info = info.findAll("td")
        if last_forecast_time:
            forecast_document["time"] = fetch_timestamp_from_date(last_forecast_time, info[0].text)
        else:
            forecast_document["time"] = fetch_timestamp_from_date(info[0].text)
        forecast_document["latitude"] = info[1].text
        forecast_document["longitude"] = info[2].text
        forecast_document["intensity"] = info[3].text
        forecast_data.append(forecast_document)
    return forecast_data

# This first part fetches all the active cyclones
# from the given URL and structures into the requred format
def fetch_active_cyclones():
    cyclone_data = []
    html_body = fetch_html_content(CYCLONE_INFO_URL, {"id" : "content"}, "div", {"class" : "basin_storms"})
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
        cyclone_data.append(document)
    return cyclone_data

# can make it parallel if we want to complete them faster
# Since this is a shceduler, we don"t have any time constraints
# Identified that there are only 3 H3 elements
# Below which either a table exists or not
# Based on that, We can easily identify which table belongs to what
def fetch_details_for_active_cyclones(data):
    for document in data:
        h3_elements = fetch_html_content(get_cyclone_detail_url(document["cyclone_id"]), {"class" : "text_product_wrapper"}, "h3")
        next_elemennt_for_forecast = h3_elements[0].find_next_sibling()
        next_elemennt_for_track = h3_elements[1].find_next_sibling()
        if str(next_elemennt_for_forecast.text) != NO_DATA:
            # In Forecase, next element is forecast time
            # and next element after that is the table
            # The below substring is what we actually need
            document["forecast_time"] = next_elemennt_for_forecast.text[25:]
            table = next_elemennt_for_forecast.find_next_sibling()
            document["forecast_data"] = convert_table_to_json(table, document["forecast_time"])

        if str(next_elemennt_for_track.text) != NO_DATA:
            document["track_data"] = convert_table_to_json(next_elemennt_for_track)
    return data

def start_worker_and_fetch_data():
    data = fetch_active_cyclones()
    if len(data) == 0:
        print("There are no active cyclones at this moment")
        return None
    return fetch_details_for_active_cyclones(data)

def tranform_data_to_tuples_for_insertion(data):
    result = {"cyclone_info" : [], "track_data" : [], "forecast_data" : []}
    for document in data:
        result["cyclone_info"].append((document["cyclone_id"], document["cyclone_name"], document["region"]))
        for entry in document["track_data"]:
            result["track_data"].append((document["cyclone_id"], entry["time"], 
                    entry["latitude"], entry["longitude"], entry["intensity"]))
        for entry in document["forecast_data"]:
            result["forecast_data"].append((document["cyclone_id"], entry["time"], 
                    entry["latitude"], entry["longitude"], entry["intensity"]))
    return result


try:
    conn = pyc.connect(host="localhost", port="5432", user="postgres", password="postgres", database="cyclone-intel")
    cur = conn.cursor()
    print("Postgres is connected. Scheduler triggerred at " + str(datetime.now()))
    cyclone_data = start_worker_and_fetch_data()
    tuples = tranform_data_to_tuples_for_insertion(cyclone_data)
    execute_values(cur, INSERT_CYCLONE_INFO, tuples["cyclone_info"])
    execute_values(cur, INSERT_TRACK_DATA, tuples["track_data"])
    execute_values(cur, INSERT_FORECAST_DATA, tuples["forecast_data"])
    conn.commit()
    conn.close()
    print("Scheduler is completed at " + str(datetime.now()))
except Exception as e:
    print("Exception occured while processing " + str(e))
