from scraper import routes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os
# This config can come up from an external source
# or via command line suing Consul and Vault to handle different environments
# for simplicity, Leaving the config with the values
config = json.load(open(os.path.abspath("config.json"), "r"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config["db_url"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
