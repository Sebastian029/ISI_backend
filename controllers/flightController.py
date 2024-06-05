from models.flight import Flight
from models.airport import Airport
from models.city import City
from config import db

def create_flight(departure_airport_id, arrive_airport_id,travel_time, distance, available_seats, plane_id, airline_id, data_lotu):
    new_flight = Flight(departure_airport_id=departure_airport_id,
                            arrive_airport_id=arrive_airport_id,
                            travel_time=travel_time,
                            distance=distance,
							available_seats = available_seats,
                            plane_id=plane_id,
                            airline_id=airline_id,
                            data_lotu=data_lotu)
    
    db.session.add(new_flight)
    db.session.commit()
    return new_flight

def get_airports(airport_id):
    
    return db.session.query(
            Airport, City.city_id, City.city_name
        ).join(
            City, Airport.city_id == City.city_id
        ).filter(
            Airport.airport_id == airport_id,
        ).first()

    
def get_flight_by_data_lotu(dep_airport, arr_airport, date ):
    return db.session.query(
            Flight
        ).filter(
            Flight.departure_airport_id == dep_airport.airport_id,
            Flight.arrive_airport_id == arr_airport.airport_id,
            Flight.data_lotu == date
        ).all()

def get_flight(dep_airport, arr_airport):
    return db.session.query(
            Flight
        ).filter(
            Flight.departure_airport_id == dep_airport.airport_id,
            Flight.arrive_airport_id == arr_airport.airport_id,
        ).all()