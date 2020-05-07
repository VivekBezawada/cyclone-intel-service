from utils.generic_utils import fetch_timestamp_from_date


def tranform_data_to_tuples_for_insertion(data):
    result = {"cyclone_info": [], "track_data": [], "forecast_data": []}
    for document in data:
        result["cyclone_info"].append(
            (document["cyclone_id"], document["cyclone_name"], document["region"]))
        for entry in document["track_data"]:
            result["track_data"].append(
                (document["cyclone_id"], entry["time"], entry["latitude"], entry["longitude"], entry["intensity"]))
        for entry in document["forecast_data"]:
            result["forecast_data"].append(
                (document["cyclone_id"], entry["time"], entry["latitude"], entry["longitude"], entry["intensity"]))
    return result


def transform_table_to_json(table, last_forecast_time=None):
    forecast_data = []
    for index, info in enumerate(table.findAll("tr")):
        if index == 0:
            continue
        forecast_document = {}
        info = info.findAll("td")
        if last_forecast_time:
            forecast_document["time"] = fetch_timestamp_from_date(
                last_forecast_time, int(info[0].text))
        else:
            forecast_document["time"] = fetch_timestamp_from_date(info[0].text)
        forecast_document["latitude"] = info[1].text
        forecast_document["longitude"] = info[2].text
        forecast_document["intensity"] = info[3].text
        forecast_data.append(forecast_document)
    return forecast_data
