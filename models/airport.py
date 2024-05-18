from config import db
from models.city import City

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