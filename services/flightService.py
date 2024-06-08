from flask import jsonify, request
from config import app
from utils import token_required, role_required
from controllers.flightController import *
from controllers.planeController import *
from controllers.airportController import *
from controllers.planeController import *
from controllers.airlineController import *
from controllers.ticketController import *
from controllers.orderController import *
from controllers.followController import *
from schemas.flight_schema import *
from pydantic import ValidationError
from datetime import datetime


@app.route("/flight_register", methods=["POST"])
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

    
@app.route('/suggest_flights', methods=['GET'])
@token_required
def suggest_flights(current_user):
    # Get the last 10 orders of the user
    orders = order_by_user(current_user.user_id)

    # Get all the tickets from these orders
    # Get all the tickets from these orders
    tickets = [ticket for order in orders for ticket in order.tickets]

    # Get all the flights from these tickets
    purchased_flights = [Flight.query.get(ticket.flight_id) for ticket in tickets]

    departure_airports = [flight.departure_airport_id for flight in purchased_flights]
    arrival_airports = [flight.arrive_airport_id for flight in purchased_flights]

    most_common_departure = max(set(departure_airports), key=departure_airports.count)
    most_common_arrival = max(set(arrival_airports), key=arrival_airports.count)

    # Get all flights from the most common departure airport to the most common arrival airport
    potential_flights = Flight.query.filter_by(departure_airport_id=most_common_departure, arrive_airport_id=most_common_arrival).all()
    print(potential_flights)
    
    # Exclude the flights that the user has already purchased
    suggested_flights = [flight for flight in potential_flights if flight not in purchased_flights]

    # Limit the suggestions to 3 flights
    suggested_flights = suggested_flights[:3]

    if suggested_flights:
        return jsonify([flight.to_json() for flight in suggested_flights]), 200
    else:
        return jsonify({"message": "No suggested flights found"}), 404



@app.route('/flights_with_airports', methods=['GET'])
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

    airports_dep = get_airports(data.departure_airport_id)
    airports_arr = get_airports(data.arrive_airport_id)

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


@app.route('/flights_with_airports_token', methods=['GET'])
@token_required
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

    airports_dep = get_airports(data.departure_airport_id)
    airports_arr = get_airports(data.arrive_airport_id)

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