from config import db
from models.ticket import Ticket

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    full_price = db.Column(db.Float, nullable=False)
    is_payment_completed = db.Column(db.Boolean, nullable=False)

    tickets = db.relationship('Ticket', backref='order', lazy=True)

    def __init__(self, user_id, full_price=0.0, is_payment_completed=False):
        self.user_id = user_id
        self.full_price = full_price
        self.is_payment_completed = is_payment_completed

    def to_json(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "full_price": self.full_price,
            "is_payment_completed": self.is_payment_completed
        }