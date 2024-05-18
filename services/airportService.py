from config import app, db
from controllers.airportController import *
from flask import  jsonify

@app.route("/airports", methods=["GET"])
def get_airports():
    airports = get_all_airports_json()
    return jsonify(airports)

@app.route("/city_airports", methods=["GET"])
def get_city_with_airport():
    try:
        city_airports = get_cities_aiports()
        return jsonify(city_airports)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
