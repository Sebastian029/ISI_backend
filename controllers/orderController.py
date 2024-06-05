from models.order import Order
from config import db
from flask import jsonify

def create_order(user_id, full_price, is_payment_completed):
    new_order = Order(user_id=user_id, full_price=full_price, is_payment_completed=is_payment_completed)
    
    db.session.add(new_order)
    db.session.commit()
    return new_order

def get_order_by_id(order_id):
    order = Order.query.get(order_id)
    if not order:
        raise ValueError(f"Order with id {order_id} not found")
    return order

def get_order_by_user_id(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    if not orders:
        raise ValueError(f"Orders with user_id = {user_id} not found")
    return orders

def get_order_tickets(order_id):
        order = get_order_by_id(order_id)
        return jsonify(order.to_json())

def get_orders_user_tickets(user_id):   
    orders = get_order_by_user_id(user_id)
    orders_with_tickets = [order.to_json() for order in orders]
    return orders_with_tickets

def get_transfer_uncompleted_orders():
    orders = Order.query.filter_by(paymentMethod='transfer', is_payment_completed=False).all()
    if not orders:
        raise ValueError(f"Orders not found")
    orders_json = [order.to_json_with_user() for order in orders]
    return orders_json


