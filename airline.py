from config import app, db
from models import  Airlines
from flask import request, jsonify

@app.route("/airlines", methods=["GET"])
def get_airlines():
    airlines = Airlines.query.all()
    json_airlines = [
        {
            "airline_name": airline.airline_name,
        }
        for airline in airlines
    ]
    return jsonify(json_airlines)