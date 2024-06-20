from flask import jsonify, request, blueprints
from app.utils import token_required, role_required
from app.controllers.flightController import *
from app.controllers.planeController import *
from app.controllers.airportController import *
from app.controllers.planeController import *
from app.controllers.airlineController import *
from app.controllers.ticketController import *
from app.controllers.orderController import *
from app.controllers.followController import *
from app.schemas.flight_schema import *
from pydantic import ValidationError
from datetime import datetime
from sqlalchemy.orm import aliased
import random

fligtbp = blueprints.Blueprint('fligtbp', __name__)

@fligtbp.route("/flight_register", methods=["POST"])
@token_required
@role_required('admin')
def register_flight(current_user):
    try:
        data = FlightRegisterSchema(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    if (data.departure_airport_id == data.arrive_airport_id):
        return jsonify({"message": "Wystąpił błąd, departure_airport_id nie może być taki sam jak arrive_airport_id"}), 400

    if not (get_aiport_by_id(data.departure_airport_id)):
        return jsonify({"message": "Wystąpił błąd, nie ma takiego departure_airport_id"}), 400
    
    if not ( get_aiport_by_id(data.arrive_airport_id)):
        return jsonify({"message": "Wystąpił błąd, nie ma takiego arrive_airport_id"}), 400
    
    if not ( get_plane_by_id(data.plane_id)):
        return jsonify({"message": "Wystąpił błąd, nie ma takiego plane_id"}), 400
        
    if not ( get_airline_by_id(data.airline_id)):
        return jsonify({"message": "Wystąpił błąd, nie ma takiego data.airline_id"}), 400

    available = available_seat(data.plane_id)

    try:
        
        new_flight = create_flight(departure_airport_id=data.departure_airport_id,
                            arrive_airport_id=data.arrive_airport_id,
                            travel_time=data.travel_time,
                            distance=data.distance,
							available_seats = available,
                            plane_id=data.plane_id,
                            airline_id=data.airline_id,
                            data_lotu=data.data_lotu)

        try:
            register_tickets(data.plane_id, new_flight)

            return jsonify({"message": "Nowy lot został zarejestrowany! Dodano bilety."}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Wystąpił błąd przy dodawaniu lotu do bazy danych: " + str(e)}), 400
    
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    
@fligtbp.route('/suggest_flights', methods=['GET'])
@token_required
def suggest_flights(current_user):
    def format_flight(flight):
        dep_airport = Airport.query.get(flight.departure_airport_id)
        arr_airport = Airport.query.get(flight.arrive_airport_id)
        dep_city = City.query.get(dep_airport.city_id)
        arr_city = City.query.get(arr_airport.city_id)
        
        return {
            "flight_id": flight.flight_id,
            "departure_airport": dep_airport.airport_name,
            "departure_city": dep_city.city_name,
            "arrival_airport": arr_airport.airport_name,
            "arrival_city": arr_city.city_name,
            "distance": flight.distance,
            "available_seats": flight.available_seats,
            "travel_time": flight.travel_time.strftime('%H:%M:%S'),
            "data_lotu": flight.data_lotu
        }

    orders = order_by_user(current_user.user_id)
    tickets = [ticket for order in orders for ticket in order.tickets]

    followed_flights = {follow.flight_id for follow in Follow.query.filter_by(user_id=current_user.user_id).all()}

    if len(tickets) < 5:
        all_flights = Flight.query.all()
        purchased_flights = {ticket.flight_id for ticket in tickets}
        unpurchased_unfollowed_flights = [
            flight for flight in all_flights 
            if flight.flight_id not in purchased_flights 
            and flight.flight_id not in followed_flights 
            and flight.available_seats > 0
        ]
        if unpurchased_unfollowed_flights:
            random_flight = random.choice(unpurchased_unfollowed_flights)
            return jsonify(format_flight(random_flight)), 200
        else:
            return jsonify({"message": "No available flights found"}), 404

    last_5_tickets = tickets[-5:]
    last_5_flights = [Flight.query.get(ticket.flight_id) for ticket in last_5_tickets]

    dep_airports = [flight.departure_airport_id for flight in last_5_flights]
    arr_airports = [flight.arrive_airport_id for flight in last_5_flights]

    common_dep_airport = max(set(dep_airports), key=dep_airports.count)
    common_arr_airport = max(set(arr_airports), key=arr_airports.count)

    suggested_flights = Flight.query.filter_by(
        departure_airport_id=common_dep_airport,
        arrive_airport_id=common_arr_airport
    ).all()

    purchased_flight_ids = {ticket.flight_id for ticket in last_5_tickets}
    suggestions = [
        flight for flight in suggested_flights 
        if flight.flight_id not in purchased_flight_ids 
        and flight.flight_id not in followed_flights 
        and flight.available_seats > 0
    ]

    if not suggestions:
        dep_countries = [flight.departure_airport.city.country_id for flight in last_5_flights]
        arr_countries = [flight.arrive_airport.city.country_id for flight in last_5_flights]

        common_dep_country = max(set(dep_countries), key=dep_countries.count)
        common_arr_country = max(set(arr_countries), key=arr_countries.count)

        dep_airport_alias = aliased(Airport, name='dep_airport_alias')
        arr_airport_alias = aliased(Airport, name='arr_airport_alias')
        dep_city_alias = aliased(City, name='dep_city_alias')
        arr_city_alias = aliased(City, name='arr_city_alias')

        suggestions = Flight.query \
            .join(dep_airport_alias, Flight.departure_airport_id == dep_airport_alias.airport_id) \
            .join(dep_city_alias, dep_airport_alias.city_id == dep_city_alias.city_id) \
            .filter(dep_city_alias.country_id == common_dep_country) \
            .join(arr_airport_alias, Flight.arrive_airport_id == arr_airport_alias.airport_id, isouter=True) \
            .join(arr_city_alias, arr_airport_alias.city_id == arr_city_alias.city_id, isouter=True) \
            .filter(arr_city_alias.country_id == common_arr_country) \
            .all()

        suggestions = [
            flight for flight in suggestions 
            if flight.flight_id not in purchased_flight_ids 
            and flight.flight_id not in followed_flights 
            and flight.available_seats > 0
        ]

    suggestions = suggestions[:2]

    if suggestions:
        return jsonify([format_flight(flight) for flight in suggestions]), 200
    else:
        return jsonify({"message": "No suggested flights found"}), 404





@fligtbp.route('/flights_with_airports', methods=['GET'])
def get_flights_with_airports():
    try:
        departure_airport_id = request.args.get('departure_airport_id')
        arrive_airport_id = request.args.get('arrive_airport_id')
        data_lotu = request.args.get('data_lotu')
        
        if data_lotu:
            data = FlightSearchSchema(
                departure_airport_id=departure_airport_id,
                arrive_airport_id=arrive_airport_id,
                data_lotu=data_lotu
            )
        else:
            data = FlightSearchSchemaWithoutDate(
                departure_airport_id=departure_airport_id,
                arrive_airport_id=arrive_airport_id
            )
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    if data_lotu:
        try:
            date = datetime.strptime(data.data_lotu, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format."}), 400

    airports_dep = get_airports_by_id(data.departure_airport_id)
    airports_arr = get_airports_by_id(data.arrive_airport_id)

    if not airports_dep or not airports_arr:
        return jsonify({'error': 'Departure or arrival airport not found.'}), 404

    dep_airport, dep_city_id, dep_city_name = airports_dep
    arr_airport, arr_city_id, arr_city_name = airports_arr

    if data_lotu:
        flights = get_flight_by_data_lotu(dep_airport, arr_airport, data.data_lotu)
    else:
        flights = get_flight(dep_airport, arr_airport)

    if not flights:
        return jsonify({'error': 'No flights found for the given parameters.'}), 404

    flights_json = []

    for flight in flights:
        flights_json.append({
            "flight_id": flight.flight_id,
            "departure_airport": dep_airport.airport_name,
            "departure_city": dep_city_name,
            "arrival_airport": arr_airport.airport_name,
            "arrival_city": arr_city_name,
            "distance": flight.distance,
            "available_seats": flight.available_seats,
            "travel_time": flight.travel_time.strftime('%H:%M:%S'),
            "data_lotu": flight.data_lotu
        })

    return jsonify(flights_json), 200


@fligtbp.route('/flights_with_airports_token', methods=['GET'])
@token_required
@role_required('user')
def get_flights_with_airports_token(current_user):
    try:
        departure_airport_id = request.args.get('departure_airport_id')
        arrive_airport_id = request.args.get('arrive_airport_id')
        data_lotu = request.args.get('data_lotu')
        
        if data_lotu:
            data = FlightSearchSchema(
                departure_airport_id=departure_airport_id,
                arrive_airport_id=arrive_airport_id,
                data_lotu=data_lotu
            )
        else:
            data = FlightSearchSchemaWithoutDate(
                departure_airport_id=departure_airport_id,
                arrive_airport_id=arrive_airport_id
            )
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    if data_lotu:
        try:
            date = datetime.strptime(data.data_lotu, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format."}), 400

    airports_dep = get_airports_by_id(data.departure_airport_id)
    airports_arr = get_airports_by_id(data.arrive_airport_id)

    if not airports_dep or not airports_arr:
        return jsonify({'error': 'Departure or arrival airport not found.'}), 404

    dep_airport, dep_city_id, dep_city_name = airports_dep
    arr_airport, arr_city_id, arr_city_name = airports_arr

    if data_lotu:
        flights = get_flight_by_data_lotu(dep_airport, arr_airport, data.data_lotu)
    else:
        flights = get_flight(dep_airport, arr_airport)

    if not flights:
        return jsonify({'error': 'No flights found for the given parameters.'}), 404

    flights_json = []

    for flight in flights:
        is_follow = get_follow(current_user.user_id, flight.flight_id)
        flights_json.append({
            "flight_id": flight.flight_id,
            "departure_airport": dep_airport.airport_name,
            "departure_city": dep_city_name,
            "arrival_airport": arr_airport.airport_name,
            "arrival_city": arr_city_name,
            "distance": flight.distance,
            "available_seats": flight.available_seats,
            "travel_time": flight.travel_time.strftime('%H:%M:%S'),
            "data_lotu": flight.data_lotu,
            "is_follow": bool(is_follow),
            "follow_id":is_follow.follow_id if is_follow else None
        })

    return jsonify(flights_json), 200