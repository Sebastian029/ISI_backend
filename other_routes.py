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
            Flight.data_lotu == date
        ).all()

        json_airports_dep = [
            {
                "airport_id": airport.airport_id,
                "airport_name": airport.airport_name,
                "IATA": airport.IATA,
                "city_id": city_id,
                "city_name": city_name
            }
            for airport, city_id, city_name in airports_dep
        ]

        airports_arr = db.session.query(
            Airport, City.city_id, City.city_name
        ).join(
            City, Airport.city_id == City.city_id
        ).filter(
            Airport.airport_name == arrive_airport_name,
            Flight.data_lotu == date
        ).all()

        json_airports_arr = [
            {
                "airport_id": airport.airport_id,
                "airport_name": airport.airport_name,
                "IATA": airport.IATA,
                "city_id": city_id,
                "city_name": city_name
            }
            for airport, city_id, city_name in airports_arr
        ]

        flights_with_airports_arr = db.session.query(
            Flight
        ).filter(
            Flight.departure_airport_id == json_airports_dep[0]["airport_id"],
            Flight.arrive_airport_id == json_airports_arr[0]["airport_id"],
            Flight.data_lotu == date
        ).all()

        json_flights = [
            {
                "flight_id":flight.flight_id,
                "departure_airport_id":flight.departure_airport_id,
                "arrive_airport_id":flight.arrive_airport_id,
                "distance":flight.distance,
                "available_seats":flight.available_seats,

            }
            for flight in flights_with_airports_arr
        ]

        ticket = db.session.query(
            Ticket
        ).filter(
            Ticket.flight_id == json_flights[0]["flight_id"]
        ).all()

        json_tickets = [
            {
                "price":ticket[0].price
            }
        ]

        flights_json = [
            {
                "flight_id":json_flights[0]["flight_id"],
                "departure_airport":json_airports_dep[0]["airport_name"],
                "departure_city":json_airports_dep[0]["city_name"],
                "arrival_airport": json_airports_arr[0]["airport_name"],
                "arrival_city": json_airports_arr[0]["city_name"],
                "distance":json_flights[0]["distance"],
                "available_seats":json_flights[0]["available_seats"],
                "ticket_price":json_tickets[0]["price"]
            }
        ]

        return jsonify(flights_json), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/city", methods=["GET"])
def get_city():
    q = request.args.get("q")
    results=[]
    if q:
       results = City.query.filter(City.city_name.ilike(f"%{q}%")).order_by(City.city_name.desc()).limit(6).all()
    return jsonify(results)