from models.user import User
from config import db

def check_password_controller(user, password):
    return user.check_password(password)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_number(phone_number):
    return User.query.filter_by(phone_number=phone_number).first()

def get_user_by_id(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_user_by_search(name, surname ,email):
    user = User.query.filter_by(name=name, surname=surname, email=email).first()
    return user.to_json_privileges()


def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.to_json() for user in users]
    return users

def get_users_search():
    users = User.query.all()
    if not users:
        return []
    users = [user.to_json_search() for user in users]
    return users


def get_user_by_public_id(public_id):
    return User.query.filter_by(public_id=public_id).first()

def get_data_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.to_json_privileges() for user in users]
    return users

def update_user(id, public_id, name, surname, phone_number, email):
    user = get_user_by_id(id)
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
    user = get_user_by_id(user_id)

    if not user:
        return False

    db.session.delete(user)
    db.session.commit()

    return True
