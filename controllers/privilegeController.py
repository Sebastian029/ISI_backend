from models.privilege import Privilege
from config import db
from controllers.userController import get_user_by_public_id
from models.user import User

def get_privilages(): 
    return Privilege.query.all()

def get_privilege_by_name(name):
    return Privilege.query.filter_by(name=name).first()

def get_privilages_json():
    privilages = Privilege.query.all()
    if not privilages:
        return []
    privilages = [privilage.to_json() for privilage in privilages]
    return privilages

def remove_privilege(public_id, privilege_name):
    user = get_user_by_public_id(public_id)
    if not user:
        return "User not found", 404

    privilege = get_privilege_by_name(privilege_name)
    if not privilege:
        return "Privilege not found", 404

    if privilege not in user.privileges:
        return "User does not have this privilege", 400

    user.privileges.remove(privilege)
    db.session.commit()

    return "Privilege removed successfully", 200

def add_privilege(public_id, privilege_name):
    user = get_user_by_public_id(public_id)
    if not user:
        return "User not found", 404

    privilege = get_privilege_by_name(privilege_name)
    if not privilege:
        return "Privilege not found", 404

    if privilege in user.privileges:
        return "User already has this privilege", 400

    user.privileges.append(privilege)
    db.session.commit()

    return "Privilege added successfully", 200
    
