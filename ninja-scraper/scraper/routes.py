from scraper import app
from flask import jsonify
from scraper.tasker import run_scheduler
def object_to_json(data):
    return [_temp.toJSON() for _temp in data]

# # This tells the user / anyone who is calling
# # whether the service is up and healthy
@app.route("/sanity")
def fetch_service_status():
    return {"status": "up", "version": "1.0"}

@app.route("/schedule")
def run_background_schedule():
    run_scheduler()
    return {"status": "success", "version": "1.0", "data" : "Job started!"}
