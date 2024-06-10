from models.airport import Airport
from models.city import City
from config import db

def get_all_airports_json():
    airports = Airport.query.all()
    if not airports:
        raise ValueError(f"Airports not found")
    airports = [airport.to_json() for airport in airports]
    return airports

def get_airports_by_id(airport_id):
    airports = db.session.query(
            Airport, City.city_id, City.city_name
        ).join(
            City, Airport.city_id == City.city_id
        ).filter(
            Airport.airport_id == airport_id,
        ).first()
    if airports is None:
        raise ValueError(f"Airports not found")
    return airports
        

def get_cities():
    result = db.session.query(
            Airport, City
        ).join(
            City, Airport.city_id == City.city_id
        ).all()
    if result is None:
        raise ValueError(f"Cities not found")
    return result

def get_aiport_by_id(id):
    return Airport.query.get(id)

def get_cities_aiports():
    results = get_cities()
    json_city_airports = [
            {
                "airport": city.city_name + " : " + airport.airport_name,
                "airport_id": airport.airport_id,
                "city_id": city.city_id
            }
            for airport, city in results
        ]
    return json_city_airports