from models.role import Role
from config import db

def get_role(id):
    return Role.query.get(id)

def all_get_role(user):
    return [role.name for role in user.roles]