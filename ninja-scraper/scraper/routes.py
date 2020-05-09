from scraper import app, db
from scraper.tasker import run_scheduler
from scraper.models import CycloneInfo
from pprint import pprint
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    data = run_scheduler()
    if (timestamp):
        data["track_data"] = list(filter(lambda _temp : _temp["synoptic_time"] > float(timestamp), data["track_data"]))
        data["forecast_data"] = list(filter(lambda _temp : _temp["forecast_time"] > float(timestamp), data["forecast_data"]))
    db.engine.execute(CycloneInfo.__table__.insert(), data["cyclone_info"])
    db.engine.execute(CycloneInfo.__table__.insert(), data["track_data"])
    db.engine.execute(CycloneInfo.__table__.insert(), data["forecast_data"])
    return {"status": "success", "version": "1.0", "data" : "Job completed!"}
