from flask import request, jsonify
from config import app, db
from models import User

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



# @app.route("/update_contact/<int:user_id>", methods=["PATCH"])
# def update_contact(user_id):
#     contact = Contact.query.get(user_id)

#     if not contact:
#         return jsonify({"message": "User not found"}), 404

#     data = request.json
#     contact.first_name = data.get("firstName", contact.first_name)
#     contact.last_name = data.get("lastName", contact.last_name)
#     contact.email = data.get("email", contact.email)

#     db.session.commit()

#     return jsonify({"message": "Usr updated."}), 200


# @app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
# def delete_contact(user_id):
#     contact = Contact.query.get(user_id)

#     if not contact:
#         return jsonify({"message": "User not found"}), 404

#     db.session.delete(contact)
#     db.session.commit()

#     return jsonify({"message": "User deleted!"}), 200


@app.route("/")
def init():
    return "Hello WORLD"


@app.route("/users", methods=["GET"])
def get_contacts():
    users = User.query.all()
    json_users = list(map(lambda x: x.to_json(), users))
    print(json_users)
    return jsonify(json_users)

@app.route('/flights', methods=['GET'])
def get_flights():
    # Pobieranie danych z zapytania
    departure_city_name = request.args.get('departure_city_name')
    arrive_city_name = request.args.get('arrive_city_name')

    # Znajdowanie miast na podstawie nazw
    departure_city = City.query.filter_by(city_name=departure_city_name).first()
    arrive_city = City.query.filter_by(city_name=arrive_city_name).first()

    if not departure_city or not arrive_city:
        return jsonify({'message': 'One or both cities not found'}), 404

    # Znajdowanie lotnisk dla podanych miast
    departure_airports = Airport.query.filter_by(city_id=departure_city.city_id).all()
    arrive_airports = Airport.query.filter_by(city_id=arrive_city.city_id).all()

    # Znajdowanie lotów na podstawie lotnisk
    flights = Flight.query.filter(
        Flight.departure_airport_id.in_([airport.airport_id for airport in departure_airports]),
        Flight.arrive_airport_id.in_([airport.airport_id for airport in arrive_airports])
    ).all()

    # Konwersja wyników do formatu JSON
    flights_json = [flight.to_json() for flight in flights]

    return jsonify(flights_json), 200





if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)