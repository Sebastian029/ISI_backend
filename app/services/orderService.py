from flask import request, jsonify
from app.config import app, db
from app.controllers.orderController import *
from app.utils import token_required, role_required
from app.schemas.order_schema import *
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


@app.route('/order/<int:order_id>', methods=['GET'])
def get_order_tickets_route(order_id):
    try:
        order = get_order_tickets(order_id)
        return order
    except ValueError as e:
        print(f"Error: {e}")  
        return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        print(f"Unexpected error: {e}")  
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/orders/user/', methods=['GET'])
@token_required
def get_orders_tickets_route(current_user):
    try:
        orders = get_orders_user_tickets(current_user.user_id)
        return orders
    except ValueError as e:
        print(f"Error: {e}")  
        return jsonify({'error': 'Orders not found'}), 404
    except Exception as e:
        print(f"Unexpected error: {e}")  
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/orders/transfer', methods=['GET'])
def get_orders_transfer_route():
    try:
        orders = get_transfer_uncompleted_orders()
        return orders
    except ValueError as e:
        print(f"Error: {e}")  
        return jsonify({'error': 'Orders not found'}), 404
    except Exception as e:
        print(f"Unexpected error: {e}")  
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/order/confirm/<int:order_id>', methods=['GET'])
def confirm_order_route(order_id):
    try:
        order = get_order_by_id(order_id)
        if order.is_payment_completed == 1:
            message = 'Payment is already completed.'
        else:
            order.is_payment_completed = 1
            db.session.commit()  
            message = 'Payment has been completed successfully.'
        return jsonify({'message': message})
    except ValueError as e:
        print(f"Error: {e}") 
        return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        print(f"Unexpected error: {e}")  
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
# @app.route('/transfer/data', methods=['POST'])
# def get_transfer_data_route():
#     try:
#         data = request.json
#         order_id = data.get('order_id')
#         order = get_order_by_id(order_id)
#         return jsonify({'full price':order.full_price, })
#     except ValueError as e:
#         print(f"Error: {e}")  
#         return jsonify({'error': 'Orders not found'}), 404
#     except Exception as e:
#         print(f"Unexpected error: {e}")  
#         return jsonify({'error': 'An unexpected error occurred'}), 500