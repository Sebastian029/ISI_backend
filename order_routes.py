import datetime
from flask import request, jsonify
from config import app, db
from models import Order, Ticket
from utils import token_required, role_required

@app.route('/order', methods=['POST'])
@token_required
@role_required('admin')
def create_order(current_user):
    data = request.json
    full_price = data.get("full_price")
    is_payment_completed = data.get("is_payment_completed")

    new_order = Order(user_id=current_user.user_id, full_price=full_price, is_payment_completed=is_payment_completed) 

    db.session.add(new_order)  
    db.session.commit() 

    return jsonify({'message' : 'New order created'})

@app.route("/")
def init():
    return "Hello WORLD"