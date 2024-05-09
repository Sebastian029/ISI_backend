from config import app, db
from models import  Flight, Airport, Plane, Airlines
from flask import request, jsonify

from config import app, db
from models import Flight, Airport, Plane, Airlines, Ticket
from flask import request, jsonify

@app.route("/flight_register", methods=["POST"])
def register_flight():
    data = request.json
    departure_airport_name = data.get("departure_airport")
    arrive_airport_name = data.get("arrive_airport")
    travel_time = data.get("travel_time")
    distance = data.get("distance")
    plane_name = data.get("plane_name")
    airline_name = data.get("airline_name")
    data_lotu = data.get("data_lotu")

    if not all([departure_airport_name, arrive_airport_name, travel_time, distance, plane_name, airline_name, data_lotu]):
        return jsonify({"message": "You must include all required fields: departure_airport_name, arrive_airport_name, travel_time, distance, plane_name, airline_name, data_lotu"}), 400

    departure_airport = Airport.query.filter_by(airport_name=departure_airport_name).first()
    arrive_airport = Airport.query.filter_by(airport_name=arrive_airport_name).first()

    plane = Plane.query.filter_by(plane_name=plane_name).first()
    airline = Airlines.query.filter_by(airline_name=airline_name).first()

    avaiable = plane.seat_rows_bis*plane.seat_columns_bis + plane.seat_rows_eco*plane.seat_columns_eco

    if departure_airport and arrive_airport and plane and airline:
        # Tworzenie nowego lotu
        new_flight = Flight(departure_airport_id=departure_airport.airport_id,
                            arrive_airport_id=arrive_airport.airport_id,
                            travel_time=travel_time,
                            distance=distance,
							available_seats = avaiable,
                            plane_id=plane.plane_id,
                            airline_id=airline.airline_id,
                            data_lotu=data_lotu)

        try:
            db.session.add(new_flight)
            db.session.commit()

            # Pobieramy informacje o liczbie rzędów i kolumn z samolotu
            rows_bis = plane.seat_rows_bis
            columns_bis = plane.seat_columns_bis
            rows_eco = plane.seat_rows_eco
            columns_eco = plane.seat_columns_eco

            # Dodajemy bilety dla klasy biznesowej
            for row in range(1, rows_bis + 1):
                for column in range(1, columns_bis + 1):
                    row_label =chr(ord('A') + row - 1) + chr(ord('A') + row - 1)  # Numer rzędu w klasie biznesowej zaczyna się od 'A'
                    new_ticket = Ticket(flight_id=new_flight.flight_id,
                                        price=100.0,  # Cena może być dowolna, tutaj jest przykładowa
                                        ticket_class="Business",  # Klasa biletu
                                        row=row_label,
                                        column=column,
                                        is_bought=1)
                    db.session.add(new_ticket)

            # Dodajemy bilety dla klasy ekonomicznej
            for row in range(1, rows_eco + 1):
                for column in range(1, columns_eco + 1):
                    row_label = chr(ord('A') + row - 1) # Numer rzędu w klasie ekonomicznej zaczyna się od 'A'
                    new_ticket = Ticket(flight_id=new_flight.flight_id,
                                        price=50.0,  # Cena może być dowolna, tutaj jest przykładowa
                                        ticket_class="Economy",  # Klasa biletu
                                        row=row_label,
                                        column=column,
                                        is_bought=1)
                    db.session.add(new_ticket)

            db.session.commit()
            return jsonify({"message": "Nowy lot został zarejestrowany! Dodano bilety."}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Wystąpił błąd przy dodawaniu lotu do bazy danych: " + str(e)}), 400
    else:
        return jsonify({"message": "Nie znaleziono jednego lub obu lotnisk o podanej nazwie, samolotu lub linii lotniczej."}), 404
