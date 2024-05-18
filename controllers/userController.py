from models.user import User
from config import db
from controllers.roleController import get_role

def create_user( firstName, lastName, phone_number, email, password):
    new_user = User(name=firstName, surname=lastName, phone_number=phone_number, email=email, password=password)
    role_id = 2
    role = get_role(role_id)
    if role:
        new_user.roles.append(role)
    
    db.session.add(new_user)
    db.session.commit()
    return new_user

def check_password_controller(user, password):
    return user.check_password(password)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_number(phone_number):
    return User.query.filter_by(phone_number=phone_number).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()


def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.to_json() for user in users]
    return users

def update_user(id, public_id, name, surname, phone_number, email):
    user = get_user(id)
    if user:
        user.public_id = public_id
        user.name = name
        user.surname = surname
        user.phone_number = phone_number
        user.email = email
        db.session.commit()
        return user
    return None

def delete_user(user_id):
    user = get_user(user_id)

    if not user:
        return False

    db.session.delete(user)
    db.session.commit()

    return True