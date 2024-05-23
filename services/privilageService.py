from config import app, db
from controllers.privilegeController import *
from controllers.userController import get_data_users_json
from flask import  jsonify

@app.route("/privilages", methods=["GET"])
def get_privilages_route():
    priviliges = get_privilages_json()
    return jsonify(priviliges)

@app.route("/users/privilages", methods=["GET"])
def get_users_privilages_route():
    users = get_data_users_json()
    return jsonify(users)