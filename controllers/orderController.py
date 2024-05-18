from models.order import Order
from config import db

def create_order(user_id, full_price, is_payment_completed):
    new_order = Order(user_id=user_id, full_price=full_price, is_payment_completed=is_payment_completed)
    
    db.session.add(new_order)
    db.session.commit()
    return new_order