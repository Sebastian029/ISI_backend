import datetime
import jwt
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email_address import validate_email
from config import app, db
from models import User, Role
from utils import token_required
import uuid

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")
    phone_number = data.get("phoneNumber")
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    if not all([first_name, last_name, email, phone_number, hashed_password]):
        return jsonify({"message": "You must include all required fields: first name, last name, email, phone number, password"}), 400

    if not validate_email(email):
        return jsonify({"message": "Invalid email address format"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    if   len(phone_number) != 9:
        return jsonify({"message": "Invalid phone number format. Phone number should be 9 digits long"}), 400

    existing_phone = User.query.filter_by(phone_number=phone_number).first()
    if existing_phone:
        return jsonify({"message": "Number already exists"}), 400

    new_user = User(
        public_id=str(uuid.uuid4()),
        name=first_name,
        surname=last_name,
        email=email,
        phone_number=phone_number,
        password=hashed_password,
        
    )
    role_id = 2 
    role = Role.query.get(role_id)
    print(role)
    new_user.roles.append(role)

    

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = User.query.get(user_id)

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

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if check_password_hash(user.password, password):
        roles = [role.name for role in user.roles]
        print("Role użytkownika:", roles)
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")

        return jsonify({'token': token, 'roles': roles})
    
    return jsonify({'message': 'Nieprawidłowe dane logowania'}), 401

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = User.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200

@app.route("/users", methods=["GET"])
def get_contacts():
    users = User.query.all()
    json_users = list(map(lambda x: x.to_json(), users))
    return jsonify(json_users)