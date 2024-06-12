from app.models.user import User
from app.config import db

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
    user = User.query.filter_by(public_id=public_id).first()
    if user is None:
        return None
    return user

def get_data_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.to_json_privileges() for user in users]
    return users

def delete_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return False

    db.session.delete(user)
    db.session.commit()

    return True

def change_notification(user):
    user.notification = not user.notification
    db.session.commit()
    return user

def change_data(data, user):
    if data.phoneNumber:
        user.phone_number = data.phoneNumber
    if data.name:
        user.name = data.name
    if data.surname:
        user.surname = data.surname
    db.session.commit()
    return user
    