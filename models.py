from config import db

class Country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(255), nullable=False)
    UTC = db.Column(db.String(10), nullable=False)

    def to_json(self):
        return {
            "country_id": self.country_id,
            "country_name": self.country_name,
            "UTC": self.UTC
        }

class City(db.Model):
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(255), nullable=False)
    airport_code = db.Column(db.String(10), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    country = db.relationship('Country', backref='cities')

    def to_json(self):
        return {
            "city_id": self.city_id,
            "city_name": self.city_name,
            "airport_code": self.airport_code,
            "country_id": self.country_id
        }

class Airport(db.Model):
    airport_id = db.Column(db.Integer, primary_key=True)
    airport_name = db.Column(db.String(255), nullable=False)
    IATA = db.Column(db.String(3), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    city = db.relationship('City', backref='airports')

    def to_json(self):
        return {
            "airport_id": self.airport_id,
            "airport_name": self.airport_name,
            "IATA": self.IATA,
            "city_id": self.city_id
        }

class Plane(db.Model):
    plane_id = db.Column(db.Integer, primary_key=True)
    plane_name = db.Column(db.String(255), nullable=False)
    seat_rows = db.Column(db.Integer, nullable=False)
    seat_columns = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            "plane_id": self.plane_id,
            "plane_name": self.plane_name,
            "seat_rows": self.seat_rows,
            "seat_columns": self.seat_columns
        }

class Airlines(db.Model):
    airline_id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {
            "airline_id": self.airline_id,
            "airline_name": self.airline_name
        }



class Flight(db.Model):
    flight_id = db.Column(db.Integer, primary_key=True)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airport.airport_id'), nullable=False)
    arrive_airport_id = db.Column(db.Integer, db.ForeignKey('airport.airport_id'), nullable=False)
    travel_time = db.Column(db.Time, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    plane_id = db.Column(db.Integer, db.ForeignKey('plane.plane_id'), nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.airline_id'), nullable=False)
    data_lotu = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            "flight_id": self.flight_id,
            "departure_airport_id": self.departure_airport_id,
            "arrive_airport_id": self.arrive_airport_id,
            "travel_time": str(self.travel_time),
            "distance": self.distance,
            "available_seats": self.available_seats,
            "plane_id": self.plane_id,
            "airline_id": self.airline_id,
            "data_lotu": self.data_lotu
        }

class Role_Users(db.Model):
    __tablename__ = 'role_users'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False, primary_key=True)
    
    def to_json(self):
        return {
            "user_id": self.user_id,
            "role_id":self.role_id
        }
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary='role_users', backref='roled')
    users = db.relationship('Order', backref='user', lazy=True)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "public_id":self.public_id,
            "name": self.name,
            "surname": self.surname,
            "phone_number": self.phone_number,
            "email": self.email,
            "password": self.password
        }

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def to_json(self):
        return {
            "role_id": self.user_id,
            "name":self.name,
        }
    
class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.flight_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    is_bought = db.Column(db.Boolean, nullable=False, default=False)  
    price = db.Column(db.Float, nullable=False)
    ticket_class = db.Column(db.String(50), nullable=False)
    
    def to_json(self):
        return {
            "ticket_id": self.ticket_id,
            "flight_id": self.flight_id,
            "order_id": self.order_id,
            "is_bought": self.is_bought,  
            "price": self.price,
            "ticket_class": self.ticket_class,
        }

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    full_price = db.Column(db.Float, nullable=False)
    is_payment_completed = db.Column(db.Boolean, nullable=False)

    tickets = db.relationship('Ticket', backref='order', lazy=True)

    def to_json(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "full_price": self.full_price,
            "is_payment_completed": self.is_payment_completed
        }