from flask import Flask
import json

# This config can come up from an external source
# or via command line suing Consul and Vault to handle different environments
# for simplicity, Leaving the config with the values
config = json.load(open('./config.json', 'r'))

app = Flask(__name__)

# This tells the user / anyone who is calling whether the service
# is up and healthy
@app.route("/sanity")
def fetch_service_status():
    return {"status" : "active"}

if __name__ == "__main__":
    app.run(debug=config['debug'], port=config['port'])