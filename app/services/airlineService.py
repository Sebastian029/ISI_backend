from app.controllers.airlineController import *
from flask import blueprints

airlinebp = blueprints.Blueprint('airlinebp', __name__)

@airlinebp.route("/airlines", methods=["GET"])
def get_airlines():
    try:
        airlines = get_all_airlines_json()
        return airlines
    except ValueError as e:
        return str(e), 404