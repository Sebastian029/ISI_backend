from config import db

class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.flight_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    is_bought = db.Column(db.Boolean, nullable=False, default=False)  
    price = db.Column(db.Float, nullable=False)
    ticket_class = db.Column(db.String(50), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            "ticket_id": self.ticket_id,
            "flight_id": self.flight_id,
            "order_id": self.order_id,
            "is_bought": self.is_bought,  
            "price": self.price,
            "ticket_class": self.ticket_class,
            "row": self.row,
            "column": self.column
        }