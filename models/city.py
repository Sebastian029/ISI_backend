from config import db
from models.country import Country

class City(db.Model):
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(255), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    country = db.relationship('Country', backref='cities')

    def to_json(self):
        return {
            "city_id": self.city_id,
            "city_name": self.city_name,
            "airport_code": self.airport_code,
            "country_id": self.country_id
        }