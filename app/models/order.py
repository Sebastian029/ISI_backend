from app.config import db
from app.models.airport import Airport
from app.models.city import City
from app.models.flight import Flight
from app.models.ticket import Ticket

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    full_price = db.Column(db.Float, nullable=False)
    is_payment_completed = db.Column(db.Boolean, nullable=False)
    paymentMethod = db.Column(db.String(50), nullable=False)
    orderDate = db.Column(db.DateTime, nullable=False)

    tickets = db.relationship('Ticket', backref='order', lazy=True)
    user = db.relationship('User', backref='orders', lazy=True)

    def __init__(self, user_id, paymentMethod, orderDate, full_price=0.0, is_payment_completed=False):
        self.user_id = user_id
        self.full_price = full_price
        self.is_payment_completed = is_payment_completed
        self.paymentMethod = paymentMethod
        self.orderDate = orderDate

    def to_json(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "full_price": self.full_price,
            "is_payment_completed": self.is_payment_completed,
            "paymentMethod": self.paymentMethod,
            "orderDate": self.orderDate,
            "tickets": [self.ticket_to_json(ticket) for ticket in self.tickets]
        }
    
    def to_json_with_user(self):
        return {
            "order_id": self.order_id,
            "full_price": self.full_price,
            "paymentMethod": self.paymentMethod,
            "orderDate": self.orderDate,
            "user": self.user.to_json() if self.user else None,
        }

    def ticket_to_json(self, ticket):
        flight = Flight.query.get(ticket.flight_id)
        departure_airport = Airport.query.get(flight.departure_airport_id)
        arrive_airport = Airport.query.get(flight.arrive_airport_id)
        departure_city = City.query.get(departure_airport.city_id)
        arrive_city = City.query.get(arrive_airport.city_id)


        return {
            "ticket_id": ticket.ticket_id,
            "flight_id": ticket.flight_id,
            "order_id": ticket.order_id,
            "is_bought": ticket.is_bought,
            "price": ticket.price,
            "ticket_class": ticket.ticket_class,
            "row": ticket.row,
            "column": ticket.column,
            "departure_airport": departure_airport.airport_name,
            "departure_city": departure_city.city_name,
            "arrive_airport": arrive_airport.airport_name,
            "arrive_city": arrive_city.city_name,
            "data_lotu": flight.data_lotu
        }