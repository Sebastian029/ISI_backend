from app.config import db

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