from app.models.role import Role
from app.config import db

def get_role(id):
    return Role.query.get(id)

def get_role_by_name(name):
    return Role.query.get(name)

def all_get_role(user):
    return [role.name for role in user.roles]