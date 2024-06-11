from app.config import app, db
from app.controllers.privilegeController import *
from app.controllers.userController import get_data_users_json
from flask import  jsonify,request
from app.utils import token_required, role_required

@app.route("/privilages", methods=["GET"])
@token_required
@role_required('admin')
def get_privilages_route(current_user):
    priviliges = get_privilages_json()
    return jsonify(priviliges)


@app.route("/users/privilages", methods=["GET"])
@token_required
@role_required('admin')
def get_users_privilages_route(current_user):
    users = get_data_users_json()
    return jsonify(users)

@app.route("/users/privileges/add", methods=["POST"])
@token_required
@role_required('admin')
def add_user_privilege_route(current_user):
    data = request.json
    public_id = data.get('public_id')
    privilege_name = data.get('privilege_name')

    if not public_id or not privilege_name:
        return jsonify({'message': 'public_id and privilege_name are required'}), 400

    message, status_code = add_privilege(public_id, privilege_name)
    return jsonify({'message': message}), status_code

@app.route("/users/privileges/remove", methods=["DELETE"])
@token_required
@role_required('admin')
def remove_user_privilege_route(current_user):
    data = request.json
    public_id = data.get('public_id')
    privilege_name = data.get('privilege_name')

    if not public_id or not privilege_name:
        return jsonify({'message': 'public_id and privilege_name are required'}), 400

    message, status_code = remove_privilege(public_id, privilege_name)
    return jsonify({'message': message}), status_code

@app.route("/")
def initddd():
    return "Hello WORLD"