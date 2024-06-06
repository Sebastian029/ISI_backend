from config import db

class Follow(db.Model):
    follow_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.flight_id'), nullable=False)

    
    def __init__(self, user_id, flight_id):
        self.user_id = user_id
        self.flight_id = flight_id

    def to_json(self):
        return {
            "follow_id": self.follow_id,
            "user_id": self.user_id,
            "flight_id": self.flight_id
        }
