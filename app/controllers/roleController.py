from app.models.role import Role
from app.config import db
from app.controllers.userController import get_user_by_public_id

def get_role(id):
    return Role.query.get(id)

def get_role_by_name(name):
    print(name)
    return Role.query.filter_by(name=name).first()

def all_get_role(user):
    return [role.name for role in user.roles]

def get_roles_json():
    roles = Role.query.all()
    if not roles:
        return []
    roles = [role.to_json() for role in roles]
    return roles

def change_role(public_id, role_name):
    user = get_user_by_public_id(public_id)
    if not user:
        return "User not found", 404

    role = get_role_by_name(role_name)
    if not role:
        return "Role not found", 404

    user.roles = [role]
    db.session.commit()

    return "Role changed successfully", 200