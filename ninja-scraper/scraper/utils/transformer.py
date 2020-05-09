from scraper.utils.generic_utils import fetch_timestamp_from_date


def tranform_data_to_tuples_for_insertion(data):
    result = {"cyclone_info": [], "track_data": [], "forecast_data": []}
    for document in data:
        result["cyclone_info"].append(
            {"cyclone_id": document["cyclone_id"], "cyclone_name": document["cyclone_name"], "region": document["region"]})
        for entry in document["track_data"]:
            result["track_data"].append(entry)
        for entry in document["forecast_data"]:
            result["forecast_data"].append(entry)
    return result


def transform_table_to_json(cyclone_id, table, last_forecast_time=None):
    forecast_data = []
    for index, info in enumerate(table.findAll("tr")):
        if index == 0:
            continue
        forecast_document = {}
        info = info.findAll("td")
        if last_forecast_time:
            forecast_document["predicted_time"] = fetch_timestamp_from_date(
                last_forecast_time, int(info[0].text))
            forecast_document["forecast_time"] = fetch_timestamp_from_date(
                last_forecast_time)
        else:
            forecast_document["synoptic_time"] = fetch_timestamp_from_date(
                info[0].text)
        forecast_document["latitude"] = float(info[1].text)
        forecast_document["longitude"] = float(info[2].text)
        forecast_document["intensity"] = float(info[3].text)
        forecast_document["cyclone_id"] = cyclone_id
        forecast_data.append(forecast_document)
    return forecast_data


def validate_forecast_data(data):
    exclude_zero_values = []
    for document in data:
        if document["latitude"] != 0 and document["longitude"] != 0 and document["intensity"] != 0:
            exclude_zero_values.append(document)
    return exclude_zero_values
