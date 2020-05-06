from flask import Flask
import json

config = json.load(open('./config.json', 'r'))

app = Flask(__name__)

# This tells the user / anyone who is calling whether the service
# is up and healthy
@app.route("/sanity")
def fetch_service_status():
    return {"status" : "active"}

if __name__ == "__main__":
    app.run(debug=config['debug'], port=config['port'])