from app.controllers.airportController import *
from flask import  jsonify
from app.utils import token_required

from flask import blueprints

airportbp = blueprints.Blueprint('airportbp', __name__)

@airportbp.route("/airports", methods=["GET"])
@token_required
def get_airports(current_user):
    airports = get_all_airports_json()
    return jsonify(airports)

@airportbp.route("/city_airports", methods=["GET"])
def get_city_with_airport():
    try:
        city_airports = get_cities_aiports()
        return jsonify(city_airports)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
