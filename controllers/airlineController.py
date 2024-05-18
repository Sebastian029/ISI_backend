from models.airline import Airlines
from config import db

def get_airline_by_id(id):
    return Airlines.query.get(id)

def get_all_airlines_json():
    airliness = Airlines.query.all()
    if not airliness:
        return []
    airliness = [airlines.to_json() for airlines in airliness]
    return airliness