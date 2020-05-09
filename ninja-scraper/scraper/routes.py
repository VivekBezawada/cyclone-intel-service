from scraper import app, db
from scraper.tasker import run_scheduler
from scraper.models import CycloneInfo, TrackData, ForecastData
from pprint import pprint
from sqlalchemy.dialects.postgresql import insert


def object_to_json(data):
    return [_temp.toJSON() for _temp in data]

# # This tells the user / anyone who is calling
# # whether the service is up and healthy
@app.route("/sanity")
def fetch_service_status():
    return {"status": "up", "version": "1.0"}


@app.route("/schedule")
@app.route("/schedule/<timestamp>")
def run_background_schedule(timestamp=None):
    try:
        data = run_scheduler()
        if (data):
            if (timestamp):
                data["track_data"] = list(filter(
                    lambda _temp: _temp["synoptic_time"] > float(timestamp), data["track_data"]))
                data["forecast_data"] = list(filter(
                    lambda _temp: _temp["forecast_time"] > float(timestamp), data["forecast_data"]))
            pprint(data["forecast_data"])
            for model_name, key_name in zip([CycloneInfo, TrackData, ForecastData], data.keys()):
                if data[key_name]:
                    insrt_stmnt = insert(model_name).values(data[key_name])
                    db.engine.execute(insrt_stmnt.on_conflict_do_nothing())
    except Exception as e:
        # Can send an email / alert to notify the admin of this failure.
        return {"status": "failure", "version": "1.0", "data": "Job failed with exception " + str(e)}
    return {"status": "success", "version": "1.0", "data": "Job completed!"}
