from flask import request, jsonify
from config import app, db
from models import User, Airport, City, Flight, Ticket, Order
from datetime import datetime



@app.route('/flights', methods=['GET'])
def get_flights():
    try:
        departure_airport_name = request.args.get('departure_airport')
        arrive_airport_name = request.args.get('arrive_airport')
        date_str = request.args.get('data_lotu')

        date = datetime.strptime(date_str, '%Y-%m-%d')

        flights = Flight.query.filter(
            Flight.departure_airport.has(airport_name=departure_airport_name),
            Flight.arrive_airport.has(airport_name=arrive_airport_name),
            Flight.data_lotu == date
        ).all()

        flights_json = []
        for flight in flights:
            flight_data = flight.to_json()
            flight_data['departure_airport_name'] = flight.departure_airport.airport_name
            flight_data['arrive_airport_name'] = flight.arrive_airport.airport_name
            flights_json.append(flight_data)

        return jsonify(flights_json), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/flights_with_airports', methods=['GET'])
def get_flights_with_airports():
    try:
        departure_airport_name = request.args.get('departure_airport')
        arrive_airport_name = request.args.get('arrive_airport')
        date_str = request.args.get('data_lotu')

        date = datetime.strptime(date_str, '%Y-%m-%d')

        airports_dep = db.session.query(
            Airport, City.city_id, City.city_name
        ).join(
            City, Airport.city_id == City.city_id
        ).filter(
            Airport.airport_name == departure_airport_name,
        ).first()

        airports_arr = db.session.query(
            Airport, City.city_id, City.city_name
        ).join(
            City, Airport.city_id == City.city_id
        ).filter(
            Airport.airport_name == arrive_airport_name,
        ).first()

        if not airports_dep or not airports_arr:
            return jsonify({'error': 'Departure or arrival airport not found.'}), 404

        dep_airport, dep_city_id, dep_city_name = airports_dep
        arr_airport, arr_city_id, arr_city_name = airports_arr

        flights = db.session.query(
            Flight
        ).filter(
            Flight.departure_airport_id == dep_airport.airport_id,
            Flight.arrive_airport_id == arr_airport.airport_id,
            Flight.data_lotu == date
        ).all()

        if not flights:
            return jsonify({'error': 'No flights found for the given parameters.'}), 404

        flights_json = []

        for flight in flights:
            flights_json.append({
                    "flight_id":flight.flight_id,
                    "departure_airport":dep_airport.airport_name,
                    "departure_city":dep_city_name,
                    "arrival_airport":arr_airport.airport_name,
                    "arrival_city":arr_city_name,
                    "distance":flight.distance,
                    "available_seats":flight.available_seats
                }
            )

        return jsonify(flights_json), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid date format.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/city", methods=["GET"])
def get_city():
    q = request.args.get("q")
    results=[]
    if q:
       results = City.query.filter(City.city_name.ilike(f"%{q}%")).order_by(City.city_name.desc()).limit(6).all()
    return jsonify(results)

