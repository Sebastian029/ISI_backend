from config import app, db
from controllers.privilegeController import *
from controllers.userController import get_data_users_json
from flask import  jsonify,request

@app.route("/privilages", methods=["GET"])
def get_privilages_route():
    priviliges = get_privilages_json()
    return jsonify(priviliges)

@app.route("/users/privilages", methods=["GET"])
def get_users_privilages_route():
    users = get_data_users_json()
    return jsonify(users)

@app.route("/users/privileges/add", methods=["POST"])
def add_user_privilege_route():
    data = request.json
    public_id = data.get('public_id')
    privilege_name = data.get('privilege_name')

    if not public_id or not privilege_name:
        return jsonify({'message': 'public_id and privilege_name are required'}), 400

    message, status_code = add_privilege(public_id, privilege_name)
    return jsonify({'message': message}), status_code

@app.route("/users/privileges/remove", methods=["DELETE"])
def remove_user_privilege_route():
    data = request.json
    public_id = data.get('public_id')
    privilege_name = data.get('privilege_name')

    if not public_id or not privilege_name:
        return jsonify({'message': 'public_id and privilege_name are required'}), 400

    message, status_code = remove_privilege(public_id, privilege_name)
    return jsonify({'message': message}), status_code