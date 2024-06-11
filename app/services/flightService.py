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
    # Get the last 10 orders of the user
    orders = order_by_user(current_user.user_id)

    # Get all the tickets from these orders
    tickets = [ticket for order in orders for ticket in order.tickets]

    if len(tickets) < 5:
        # Jeśli użytkownik ma mniej niż 5 kupionych biletów, zwracamy losowy bilet, którego dotychczas nie kupił
        all_flights = Flight.query.all()
        purchased_flights = [ticket.flight_id for ticket in tickets]
        unpurchased_flights = [flight for flight in all_flights if flight.flight_id not in purchased_flights]
        random_flight = random.choice(unpurchased_flights)
        return jsonify(random_flight.to_json()), 200

    # Get the last 5 tickets
    last_5_tickets = tickets[-5:]

    # Get all the flights from these 5 tickets
    last_5_flights = [Flight.query.get(ticket.flight_id) for ticket in last_5_tickets]

    # Analyze the departure and arrival airports
    departure_airports = [flight.departure_airport_id for flight in last_5_flights]
    arrival_airports = [flight.arrive_airport_id for flight in last_5_flights]

    most_common_departure = max(set(departure_airports), key=departure_airports.count)
    most_common_arrival = max(set(arrival_airports), key=arrival_airports.count)

    # Suggest flights based on the most common departure and arrival airports
    potential_flights_airport = Flight.query.filter_by(departure_airport_id=most_common_departure, arrive_airport_id=most_common_arrival).all()

    # Exclude the flights that the user has already purchased
    suggested_flights_airport = [flight for flight in potential_flights_airport if flight not in last_5_flights]

    # Limit the suggestions to 2 flights
    suggested_flights_airport = suggested_flights_airport[:2]

    # Analyze the countries for departure and arrival airports
    departure_countries = [flight.departure_airport.city.country_id for flight in last_5_flights]
    arrival_countries = [flight.arrive_airport.city.country_id for flight in last_5_flights]

    most_common_departure_country = max(set(departure_countries), key=departure_countries.count)
    most_common_arrival_country = max(set(arrival_countries), key=arrival_countries.count)

    # Aliases for Airport and City tables
    dep_airport = aliased(Airport, name='dep_airport')
    arr_airport = aliased(Airport, name='arr_airport')
    dep_city = aliased(City, name='dep_city')
    arr_city = aliased(City, name='arr_city')

    # Query for potential flights
    potential_flights_country = Flight.query \
        .join(dep_airport, Flight.departure_airport_id == dep_airport.airport_id) \
        .join(dep_city, dep_airport.city_id == dep_city.city_id) \
        .join(arr_airport, Flight.arrive_airport_id == arr_airport.airport_id, isouter=True) \
        .join(arr_city, arr_airport.city_id == arr_city.city_id, isouter=True) \
        .filter(dep_city.country_id == most_common_departure_country) \
        .filter(arr_city.country_id == most_common_arrival_country) \
        .all()

    # Exclude the flights that the user has already purchased
    suggested_flights_country = [flight for flight in potential_flights_country if flight not in last_5_flights]

    # Limit the suggestions to 2 flights
    suggested_flights_country = suggested_flights_country[:1]

    # Combine the suggestions from both criteria and ensure no duplicates
    suggested_flights = list({flight.flight_id: flight for flight in suggested_flights_airport + suggested_flights_country}.values())

    if suggested_flights:
        return jsonify([flight.to_json() for flight in suggested_flights]), 200
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