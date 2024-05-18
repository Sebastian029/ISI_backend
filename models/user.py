from config import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models.role import Role
from models.roleuser import Role_Users
from models.order import Order


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password= db.Column(db.String(255), nullable=False)
    
    roles = db.relationship('Role', secondary='role_users', backref='roled')
    users = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, name, surname, phone_number, email, password):
        self.public_id = str(uuid.uuid4())
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "public_id": self.public_id,
            "name": self.name,
            "surname": self.surname,
            "phone_number": self.phone_number,
            "email": self.email,
            "password": self.password 
        }