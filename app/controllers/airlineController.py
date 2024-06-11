from app.models.airline import Airlines
from app.config import db

def get_airline_by_id( airline_id):
    airline = Airlines.query.get(airline_id)
    if airline is None:
        raise ValueError(f"Airline with id {airline_id} not found")
    return airline

def get_all_airlines_json():
    airliness = Airlines.query.all()
    if not airliness:
        raise ValueError(f"Airlines not found")
    airliness = [airlines.to_json() for airlines in airliness]
    return airliness