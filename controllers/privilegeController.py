from models.privilege import Privilege
from config import db

def get_privilages(): 
    return Privilege.query.all()

def get_privilages_json():
    privilages = Privilege.query.all()
    if not privilages:
        return []
    privilages = [privilage.to_json() for privilage in privilages]
    return privilages

