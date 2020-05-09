from app import app
from app.models import CycloneInfo, TrackData, ForecastData


def object_to_json(data):
    return [_temp.toJSON() for _temp in data]

# # This tells the user / anyone who is calling
# # whether the service is up and healthy
@app.route("/sanity")
def fetch_service_status():
    return {"status": "up", "version": "1.0"}


@app.route("/cyclones")
def fetch_active_cyclones():
    active_cyclones = CycloneInfo.query.all()
    return {"status": "success", "version": "1.0", "data": object_to_json(active_cyclones)}


@app.route("/cyclones/<cyclone_id>/track_data")
def fetch_track_data_for_given_cylone_id(cyclone_id):
    track_data = TrackData.query.filter_by(cyclone_id=cyclone_id).all()
    return {"status": "success", "version": "1.0", "data": object_to_json(track_data)}


@app.route("/cyclones/<cyclone_id>/forecast_data/<forecast_time>")
def fetch_forecast_data_for_given_cylone_id(cyclone_id, forecast_time):
    forecast_data = ForecastData.query.filter_by(
        cyclone_id=cyclone_id, forecast_time=forecast_time).all()
    # Fetching the list of predicted time to check the synoptic time
    # in track data and return both the info for comparision
    predicted_time_list = [_temp.predicted_time for _temp in forecast_data]
    track_data = TrackData.query.filter(TrackData.cyclone_id.in_(
        [cyclone_id]), TrackData.synoptic_time.in_(predicted_time_list)).all()
    return {"status": "success", "version": "1.0", "data": {"track_data": object_to_json(track_data), "forecast_data": object_to_json(forecast_data)}}
