from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import os


# create app
app = Flask(__name__)

# create the API
api = Api(app)
CORS(app)

# Presents homepage
@app.route("/")
def index():
    return "Hello World"


# # adds favicon
# @app.route("/favicon.ico")
# def favicon():
#     return send_from_directory(app.template_folder, "favicon.ico")
