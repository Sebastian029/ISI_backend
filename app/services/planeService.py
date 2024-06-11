from app.config import app, db
from app.controllers.planeController import *
from flask import jsonify



@app.route("/planes", methods=["GET"])
def get_planes():
    planes = get_all_planes_json()
    return jsonify(planes)