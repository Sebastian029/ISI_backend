from app.config import db

class Airlines(db.Model):
    airline_id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {
            "airline_id": self.airline_id,
            "airline_name": self.airline_name
        }