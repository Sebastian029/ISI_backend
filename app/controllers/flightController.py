from app.models.flight import Flight
from app.controllers.userController import get_user_by_id
from app.config import db, mail
from flask_mailman import EmailMessage
from app.controllers.followController import get_followers_by_id

def get_flight_by_id(flight_id):
    flight = Flight.query.get(flight_id)
    if flight is None:
        raise ValueError(f"Flight with id {flight_id} not found")
    return flight


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
        flight.available_seats -= remaining_tickets

        if flight.available_seats == 2 or flight.available_seats == 1:
            followers = get_followers_by_id(flight_id)
            
            for follower in followers:
                user = get_user_by_id(follower.user_id)
                if user and user.notification:
                    send_notification_email(follower.user_id, flight_id)

        if flight.available_seats == 0:
            followers = get_followers_by_id(flight_id)
            
            for follower in followers:
                user = get_user_by_id(follower.user_id)
                if user and user.notification:
                    send_cancel_email(follower.user_id, flight_id)
                
        db.session.commit()
        return {"message": f"Available seats for flight {flight_id} updated successfully"}, 200
    else:
        return {"message": f"Flight with id {flight_id} not found"}, 404


def send_notification_email(user_id, flight_id):
    try:
        user = get_user_by_id(user_id)
        flight = get_flight_by_id(flight_id)
        email = user.email
        if user and flight:
            msg = EmailMessage(
            'Hi'+ str(user.name) + ' Your flight is almost full!',
            'Hello, you are following flight from : ' + str(flight.departure_airport.airport_name) + ' to ' + str(flight.arrive_airport.airport_name) +'. The number of available seats is now: ' + str(flight.available_seats),
            'dominikjaroszek@fastmail.com',
            [str(email)],
            )
            msg.send()
            return "Email sent"
    except Exception as e:
        return str(e)

def send_cancel_email(user_id, flight_id):
    try:
        user = get_user_by_id(user_id)
        flight = get_flight_by_id(flight_id)
        email = user.email
        if user and flight:
            msg = EmailMessage(
            'Hi'+ str(user.name) + ' Your flight is full!',
            'Hello, you are following flight from : ' + str(flight.departure_airport.airport_name) + ' to ' + str(flight.arrive_airport.airport_name) +'. The number of available seats is now: ' + str(flight.available_seats),
            'dominikjaroszek@fastmail.com',
            [str(email)],
            )
            msg.send()
            return "Email sent"
    except Exception as e:
        return str(e)

    
def get_flight_by_data_lotu(dep_airport, arr_airport, date ):
    flight = db.session.query(
            Flight
        ).filter(
            Flight.departure_airport_id == dep_airport.airport_id,
            Flight.arrive_airport_id == arr_airport.airport_id,
            Flight.data_lotu == date
        ).all()
    if flight is None:
        raise ValueError(f"Flight not found")
    return flight

def get_flight(dep_airport, arr_airport):
    flight = db.session.query(
            Flight
        ).filter(
            Flight.departure_airport_id == dep_airport.airport_id,
            Flight.arrive_airport_id == arr_airport.airport_id,
        ).all()
    if flight is None:
        raise ValueError(f"Flight not found")
    return flight
    