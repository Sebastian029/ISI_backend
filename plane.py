from config import app, db
from models import  Plane
from flask import request, jsonify

@app.route("/planes", methods=["GET"])
def get_planes():
    planes = Plane.query.all()
    json_planes = [
        {
            "plane_name": plane.plane_name,
        }
        for plane in planes
    ]
    return jsonify(json_planes)