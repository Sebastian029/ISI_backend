from config import app, db
from models import  Airport
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