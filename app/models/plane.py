from app.config import db

class Plane(db.Model):
    plane_id = db.Column(db.Integer, primary_key=True)
    plane_name = db.Column(db.String(255), nullable=False)
    seat_rows_bis = db.Column(db.Integer, nullable=False)
    seat_columns_bis = db.Column(db.Integer, nullable=False)
    seat_rows_eco = db.Column(db.Integer, nullable=False)
    seat_columns_eco = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            "plane_id": self.plane_id,
            "plane_name": self.plane_name,
            "seat_rows_bis": self.seat_rows_bis,
            "seat_columns_bis": self.seat_columns_bis,
            "seat_rows_eco": self.seat_rows_eco,
            "seat_columns_eco": self.seat_columns_eco
        }
    