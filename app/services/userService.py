from flask import request, jsonify,blueprints
from app.controllers.userController import *
from app.controllers.roleUserController import *
from app.controllers.roleController import all_get_role
from app.utils import *
from app.schemas.user_schema import *
from pydantic import ValidationError
from app.config import db
from app.models.token import Token
from sqlalchemy import update
from app.controllers.tokenController import get_first_free_token_id

userbp= blueprints.Blueprint('userbp', __name__)

@userbp.route("/register", methods=["POST"])
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
            password=data.password,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201

@userbp.route('/login', methods=['POST'])
def login():
    try:
        data = UserLoginModel(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    user = get_user_by_email(data.email)
    if check_password_controller(user, data.password):
        
        roles = all_get_role(user)
        print(roles)
        access_token = generate_access_token(user.public_id, roles, user.name, user.surname)
        refresh_token = generate_refresh_token(user.public_id, roles, user.name, user.surname)
        token = Token(token_id = get_first_free_token_id(), refresh_token = refresh_token, access_token = access_token, user_id = user.user_id )
        db.session.add(token)
        db.session.commit()
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
    
    return jsonify({'message': 'Nieprawidłowe dane logowania'}), 401


@userbp.route("/notification", methods=["PATCH"])
@token_required
@role_required('user')
def update_notification(current_user):
    user = get_user_by_id(current_user.user_id)
    if user:
        user = change_notification(user)

        message = "Notifications enabled" if user.notification else "Notifications disabled"
        return jsonify({"message": message}), 200
    return jsonify({"message": "User not found"}), 404


@userbp.route("/update_user", methods=["PATCH"])
@token_required
@role_required('user')
def update_user(current_user):
    try:
        data = UserUpdateModel(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    user = get_user_by_email(current_user.email)
    if user:
        change_data(data, user)
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404



@userbp.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    if delete_user(user_id):
        return jsonify({"message": "User deleted!"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

@userbp.route("/users", methods=["GET"])
@token_required
def get_contacts(current_user):
    users = get_all_users_json()
    return jsonify(users)

@userbp.route('/logout', methods=['DELETE'])
def logout():
    access_token = None
    if 'x-access-tokens' in request.headers:
        access_token = request.headers['x-access-tokens']
    print(access_token)

    refresh_token = None    
    if 'x-refresh-tokens' in request.headers:
        refresh_token = request.headers['x-refresh-tokens']
    print(refresh_token)

    if revoke_token(access_token, refresh_token):
        return jsonify({"message": "Refresh and aceess token revoked"}),200
    
    
    return jsonify({"message": "Invalid refresh token"}), 400
    

@userbp.route('/contact', methods=['GET'])
@token_required
@role_required('user')
def get_contact(current_user):
    user = get_user_by_id(current_user.user_id)
    return jsonify(user.to_json_user())


@userbp.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.headers.get('x-refresh-tokens')
    
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 400
    
    try:
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401
    
    current_user = User.query.filter_by(public_id=data['public_id']).first()
    if current_user is None:
        return jsonify({'message': 'Invalid refresh token'}), 401
    
    stored_token = Token.query.filter_by(refresh_token=refresh_token).first()
    if not stored_token:
        return jsonify({'message': 'Invalid or expired refresh token'}), 401
    roles = all_get_role(current_user)
    
    new_access_token = generate_access_token(current_user.public_id, roles, current_user.name, current_user.surname)

    stmt = update(Token).where(Token.token_id == stored_token.token_id).values(access_token=new_access_token)
    db.session.execute(stmt)
    db.session.commit()
    return jsonify({'access_token': new_access_token})

# @app.route("/users_email", methods=["GET"])
# def get_contacts_email():
#     try:
#         name = request.args.get('name')
#         surname = request.args.get('surname')
#         email = request.args.get('email')

#         if email:
#             data = UserSearchModel(
#                 name=name,
#                 surname=surname,
#                 email=email
#             )
#         else:
#             data = UserModel(
#                 name=name,
#                 surname=surname
#             )
#     except ValidationError as e:
#         return jsonify({"message": e.errors()}), 400
    
#     if email:
#         users = get_users_by_email(data.name, data.surname ,data.email)
#     else:
#         users = get_users(data.name, data.surname)
#     return jsonify(users)


@userbp.route("/user_privileges", methods=["POST"])
@token_required
@role_required('admin')
def get_contacts_email(current_user):
    try:
         data = UserSearchModel(**request.json)
            

    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    
    user = get_user_by_search(data.name, data.surname, data.email)
    
    return jsonify(user)