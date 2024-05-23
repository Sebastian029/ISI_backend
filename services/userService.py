from flask import request, jsonify, url_for,session,redirect,json
from config import app, db,google
from controllers.userController import get_user_by_email, get_user_by_number, create_user, check_password_controller,get_user,update_user,get_all_users_json, delete_user
from controllers.roleController import all_get_role
from utils import *
from schemas.user_schema import UserRegistrationModel, UserLoginModel  
from pydantic import ValidationError
from authlib.integrations.flask_client import OAuth
import secrets


@app.route("/register", methods=["POST"])
def register_user():
    try:
        data = UserRegistrationModel(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    if get_user_by_email(data.email):
        return jsonify({"message": "Email already exists"}), 400

    if get_user_by_number(data.phoneNumber):
        return jsonify({"message": "Number already exists"}), 400

    try:
        create_user(
            firstName=data.firstName,
            lastName=data.lastName,
            email=data.email,
            phone_number=data.phoneNumber,
            password=data.password
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201

@app.route('/login', methods=['POST'])
def login():
    try:
        data = UserLoginModel(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    user = get_user_by_email(data.email)
    if check_password_controller(user, data.password):
        roles = all_get_role(user)
        access_token = generate_access_token(user.public_id)
        refresh_token = generate_refresh_token(user.public_id)

        return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'roles': roles, 'name': user.name, 'surname':user.surname}), 200
    
    return jsonify({'message': 'Nieprawidłowe dane logowania'}), 401





@app.route("/update_email/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = get_user(user_id)

    if not contact:
            return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.name = data.get("name",contact.name)
    contact.surname = data.get("lastName",contact.surname)
    contact.email = data.get("email",contact.email)
    contact.phone_number = data.get("phoneNumber",contact.phone_number)
    contact.password = data.get("password",contact.password)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200



@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    if delete_user(user_id):
        return jsonify({"message": "User deleted!"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/users", methods=["GET"])
@token_required
def get_contacts(current_user):
    users = get_all_users_json()
    return jsonify(users)

@app.route('/logout', methods=['DELETE'])
def logout():
    token = None
    if 'x-access-tokens' in request.headers:
        token = request.headers['x-access-tokens']
        
    refresh_token = None    
    if 'x-refresh-tokens' in request.headers:
        refresh_token = request.headers['x-refresh-tokens']
    if revoke_token(refresh_token,token):
        return jsonify({"message": "Refresh token revoked"})
    return jsonify({"message": "Invalid refresh token"}), 400

@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = None
    if 'x-refresh-tokens' in request.headers:
        refresh_token = request.headers['x-refresh-tokens']

    data = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=["HS256"])
    current_user = User.query.filter_by(public_id=data['public_id']).first()
    if current_user is None:
        return jsonify({'message': 'Invalid or expired refresh token'}), 401

    stored_token = RefreshToken.query.filter_by(token=refresh_token, revoked=False).first()
    if not stored_token:
        return jsonify({'message': 'Invalid or expired refresh token'}), 401

    access_token = generate_access_token(current_user.public_id)

    return jsonify({'access_token': access_token})

