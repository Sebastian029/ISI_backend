from flask import jsonify
from flask import  jsonify,request,blueprints
from app.utils import token_required, role_required
from app.controllers.userController import get_role_users_json
from app.controllers.roleController import get_roles_json, change_role

rolebp = blueprints.Blueprint('rolebp', __name__)

@rolebp.route("/users/roles", methods=["GET"])
@token_required
@role_required('admin')
def get_users_privilages_route(current_user):
    users = get_role_users_json(current_user)
    return jsonify(users)

@rolebp.route("/roles", methods=["GET"])
@token_required
@role_required('admin')
def get_privilages_route(current_user):
    roles = get_roles_json()
    return jsonify(roles)

@rolebp.route("/change_role", methods=["POST"])
@token_required
@role_required('admin')
def change_role_route(current_user):
    data = request.json
    public_id = data.get('public_id')
    role_name = data.get('role_name')

    if not public_id or not role_name:
        return jsonify({'message': 'public_id and role_name are required'}), 400

    message, status_code = change_role(public_id, role_name)
    return jsonify({'message': message}), status_code