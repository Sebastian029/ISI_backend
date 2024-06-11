from app.config import db
from app.models.airport import Airport

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

    departure_airport = db.relationship("Airport", foreign_keys=[departure_airport_id])
    arrive_airport = db.relationship("Airport", foreign_keys=[arrive_airport_id])

    def __init__(self, departure_airport_id, arrive_airport_id, travel_time, distance, available_seats, plane_id, airline_id, data_lotu):
        self.departure_airport_id = departure_airport_id
        self.arrive_airport_id = arrive_airport_id
        self.travel_time = travel_time
        self.distance = distance
        self.available_seats = available_seats
        self.plane_id = plane_id
        self.airline_id = airline_id
        self.data_lotu = data_lotu

        
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