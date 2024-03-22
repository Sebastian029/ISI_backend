from flask import request, jsonify
from config import app, db
from models import User, Airport, City, Flight, Airport
from datetime import datetime

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")
    phone_number = data.get("phoneNumber")
    password = data.get("password")

    if not all([first_name, last_name, email, phone_number, password]):
        return jsonify({"message": "You must include all required fields: first name, last name, email, phone number, password"}), 400

    new_user = User(
        name=first_name,
        surname=last_name,
        email=email,
        phone_number=phone_number,
        password=password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    # Zwrócenie wszystkich danych nowo zarejestrowanego użytkownika w formacie JSON
    return jsonify({"message": "User created!"}), 201



@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = User.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.name = data.get("name",contact.name)
    contact.surname = data.get("lastName",contact.surname)
    contact.email = data.get("email",contact.email)
    contact.phone_number = data.get("phoneNumber",contact.phone_number)
    contact.password = data.get("password",contact.password)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Sprawdzenie czy użytkownik istnieje w bazie danych
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return jsonify(user.user_id)
    else:
        return jsonify({'message': 'Nieprawidłowe dane logowania'}), 401



@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = User.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200


@app.route("/")
def init():
    return "Hello WORLD"


@app.route("/users", methods=["GET"])
def get_contacts():
    users = User.query.all()
    json_users = list(map(lambda x: x.to_json(), users))
    # print(json_users)
    return jsonify(json_users)

@app.route("/airports", methods=["GET"])
def get_ports():
    airports = db.session.query(Airport, City.city_id, City.city_name).join(City).all()
    json_airports = [
        {
            "airport_id": airport.airport_id,
            "airport_name": airport.airport_name,
            "IATA": airport.IATA,
            "city_id": city_id,
            "city_name": city_name
        }
        for airport, city_id, city_name in airports
    ]
    return jsonify(json_airports)





@app.route('/flights', methods=['GET'])
def get_flights():
    try:
        # Pobieranie danych z zapytania
        departure_airport_name = request.args.get('departure_airport')
        arrive_airport_name = request.args.get('arrive_airport')
        date_str = request.args.get('data_lotu')
        
        # Konwersja daty na obiekt datetime
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Pobranie lotów pasujących do podanych danych
        flights = Flight.query.filter(
            Flight.departure_airport.has(airport_name=departure_airport_name),
            Flight.arrive_airport.has(airport_name=arrive_airport_name),
            Flight.data_lotu == date
        ).all()

        # Konwersja znalezionych lotów na format JSON
        flights_json = []
        for flight in flights:
            flight_data = flight.to_json()
            flight_data['departure_airport_name'] = flight.departure_airport.airport_name
            flight_data['arrive_airport_name'] = flight.arrive_airport.airport_name
            flights_json.append(flight_data)

        # Zwracanie znalezionych lotów jako odpowiedź JSON
        return jsonify(flights_json), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/flights_with_airports', methods=['GET'])
def get_flights_with_airports():
    try:
        # Pobieramy dane z zapytania
        departure_airport_name = request.args.get('departure_airport')
        arrive_airport_name = request.args.get('arrive_airport')
        date_str = request.args.get('data_lotu')
        
        # Konwertujemy datę z ciągu znaków na obiekt datetime
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # Wykonujemy łączenie (join) tabeli Flight z tabelami Airport i City dla lotniska wylotowego
        flights_with_airports_dep = db.session.query(
            Flight, Airport, City.city_id, City.city_name
        ).join(
            Airport, Flight.departure_airport_id == Airport.airport_id
        ).join(
            City, Airport.city_id == City.city_id
        ).filter(
            Airport.airport_name == departure_airport_name,
            Flight.data_lotu == date
        ).all()

        # Wykonujemy łączenie (join) tabeli Flight z tabelami Airport i City dla lotniska przylotowego
        flights_with_airports_arr = db.session.query(
            Flight, Airport, City.city_id, City.city_name
        ).join(
            Airport, Flight.arrive_airport_id == Airport.airport_id
        ).join(
            City, Airport.city_id == City.city_id
        ).filter(
            Airport.airport_name == arrive_airport_name,
            Flight.data_lotu == date
        ).all()

        # Konwersja wyników na format JSON dla lotniska wylotowego
        flights_json = []
        for flight, dep_airport, dep_city_id, dep_city_name in flights_with_airports_dep:
            flight_data = flight.to_json()
            flight_data['departure_airport'] = {
                'airport_id': dep_airport.airport_id,
                'airport_name': dep_airport.airport_name,
                'IATA': dep_airport.IATA,
                'city_id': dep_city_id,
                'city_name': dep_city_name
            }
            flights_json.append(flight_data)

        # Dodanie danych o lotnisku przylotowym do flights_json
        for idx, (flight, arr_airport, arr_city_id, arr_city_name) in enumerate(flights_with_airports_arr):
            flights_json[idx]['arrival_airport'] = {
                'airport_id': arr_airport.airport_id,
                'airport_name': arr_airport.airport_name,
                'IATA': arr_airport.IATA,
                'city_id': arr_city_id,
                'city_name': arr_city_name
            }

        return jsonify(flights_json), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)