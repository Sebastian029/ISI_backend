from flask import request, jsonify
from config import app, db
from models import User, Airport, City, Flight, Airport, Ticket
from datetime import datetime
from validate_email_address import validate_email

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")
    phone_number = data.get("phoneNumber")
    password = data.get("password")

    # Sprawdzenie czy wszystkie wymagane pola są dostarczone
    if not all([first_name, last_name, email, phone_number, password]):
        return jsonify({"message": "You must include all required fields: first name, last name, email, phone number, password"}), 400

    # Walidacja adresu e-mail
    if not validate_email(email):
        return jsonify({"message": "Invalid email address format"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    if not phone_number.startswith('+48') or len(phone_number) != 12 or not phone_number[3:].isdigit():
        return jsonify({"message": "Invalid phone number format. Phone number should start with '+48' and be 9 digits long"}), 400

    # Usunięcie prefiksu kierunkowego przed zapisaniem do bazy danych
    phone_number = phone_number[3:]

    existing_phone = User.query.filter_by(phone_number=phone_number).first()
    if existing_phone:
        return jsonify({"message": "Number already exists"}), 400

    existing_phone = User.query.filter_by(phone_number=phone_number).first()
    if existing_phone:
        return jsonify({"message": "Number already exists"}), 400
    # Tutaj możesz dodać inne rodzaje walidacji, np. dla hasła

    # Jeśli dane są poprawne, tworzymy nowego użytkownika i zapisujemy go w bazie danych
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

    # Zwrócenie odpowiedzi potwierdzającej utworzenie użytkownika
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

        # Wykonujemy łączenie (join) tabeli Flight z tabelami Airport i City dla lotniska przylotowego
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

        # Konwersja wyników na format JSON dla lotniska wylotowego
        flights_json = [
            {
                "departure airport":json_airports_dep[0]["airport_name"],
                "departure city":json_airports_dep[0]["city_name"],
                "arrival airport": json_airports_arr[0]["airport_name"],
                "arrival city": json_airports_arr[0]["city_name"],
                "distance":json_flights[0]["distance"],
                "available_seats":json_flights[0]["available_seats"],
                "ticket price":json_tickets[0]["price"]
            }
        ]

        return jsonify(flights_json), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/city", methods=["GET"])
def get_city():
    q = request.args.get("q")
    print(q)
    results=[]
    if q:
       results = City.query.filter(City.city_name.ilike(f"%{q}%")).order_by(City.city_name.desc()).limit(6).all()
     
    return jsonify(results)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)