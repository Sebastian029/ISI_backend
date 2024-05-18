from config import app, db
from controllers.airlineController import *
from flask import request, jsonify



@app.route("/airlines", methods=["GET"])
def get_airlines():
    airlines = get_all_airlines_json()
    return jsonify(airlines)