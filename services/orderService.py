from flask import request, jsonify
from config import app, db
from controllers.orderController import *
from utils import token_required, role_required
from schemas.order_schema import *
from pydantic import ValidationError

@app.route('/order', methods=['POST'])
@token_required
@role_required('user')
def register_order(current_user):
    try:
        data = OrderRegistrationModel(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    try:
        create_order(user_id=current_user.user_id, full_price=data.full_price, is_payment_completed=data.is_payment_completed) 
    except Exception as e:
        return jsonify({"message": e.errors()}), 400

    return jsonify({'message' : 'New order created'})


