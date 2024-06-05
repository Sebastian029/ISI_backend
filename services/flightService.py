from flask import jsonify, request
from config import app
from utils import token_required, role_required
from controllers.flightController import *
from controllers.planeController import *
from controllers.airportController import *
from controllers.planeController import *
from controllers.airlineController import *
from controllers.ticketController import *
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