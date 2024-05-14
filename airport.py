from config import app, db
from models import Airport, City
from flask import request, jsonify

@app.route("/airports", methods=["GET"])
def get_ports():
    airports = Airport.query.all()
    json_airports = [
        {
            "airport_name": airport.airport_name,
        }
        for airport in airports
    ]
    return jsonify(json_airports)


@app.route("/city_airports", methods=["GET"])
def get_city_with_airport():
    try:
        results = db.session.query(
            Airport, City
        ).join(
            City, Airport.city_id == City.city_id
        ).all()

        json_city_airports = [
            {
                "airport": city.city_name + " : " + airport.airport_name,
            }
            for airport, city in results
        ]
        return jsonify(json_city_airports)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

