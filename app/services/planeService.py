from app.controllers.planeController import *
from flask import jsonify

from flask import blueprints

planebp = blueprints.Blueprint('planebp', __name__)

@planebp.route("/planes", methods=["GET"])
def get_planes():
    planes = get_all_planes_json()
    return jsonify(planes)