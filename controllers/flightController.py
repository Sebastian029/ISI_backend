from models.flight import Flight
from models.airport import Airport
from models.city import City
from models.follow import Follow
from controllers.userController import get_user_by_id
from config import db, mail
from flask_mailman import EmailMessage

def get_flight_by_id(flight_id):
    return Flight.query.get(flight_id)


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


def update_available_seats(flight_id, remaining_tickets):
    flight = get_flight_by_id(flight_id)
    
    if flight:
        # Zaktualizuj dostępne miejsca na locie
        flight.available_seats -= remaining_tickets

        if flight.available_seats == 2 or flight.available_seats == 1:
            followers = Follow.query.filter_by(flight_id=flight_id).all()
            
            for follower in followers:
                user = get_user_by_id(follower.user_id)
                if user and user.notification:
                    send_notification_email(follower.user_id, flight_id)

        if flight.available_seats == 0:
            followers = Follow.query.filter_by(flight_id=flight_id).all()
            
            for follower in followers:
                user = get_user_by_id(follower.user_id)
                if user and user.notification:
                    send_cancel_email(follower.user_id, flight_id)
                
        db.session.commit()
        return {"message": f"Available seats for flight {flight_id} updated successfully"}, 200
    else:
        return {"message": f"Flight with id {flight_id} not found"}, 404


def send_notification_email(user_id, flight_id):
    user = get_user_by_id(user_id)
    flight = get_flight_by_id(flight_id)
    email = user.email
    if user and flight:
        msg = EmailMessage(
        'Hello',
        'Hello, you are following flight with id: ' + str(flight_id) + '. The number of available seats is now: ' + str(flight.available_seats),
        'dominikjaroszek@fastmail.com',
        [str(email)],
        )
        msg.send()
        return "Email sent"

def send_cancel_email(user_id, flight_id):
    user = get_user_by_id(user_id)
    flight = get_flight_by_id(flight_id)
    email = user.email
    if user and flight:
        msg = EmailMessage(
        'Hello',
        'Hello, cancel with id: ',
        'dominikjaroszek@fastmail.com',
        [str(email)],
        )
        msg.send()
        return "Email sent"

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