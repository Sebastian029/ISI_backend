from models.airport import Airport
from models.city import City
from config import db

def get_all_airports_json():
    airports = Airport.query.all()
    if not airports:
        return []
    airports = [airport.to_json() for airport in airports]
    return airports

def get_cities():
    result = db.session.query(
            Airport, City
        ).join(
            City, Airport.city_id == City.city_id
        ).all()
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