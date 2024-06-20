from flask import jsonify, request, url_for, redirect
from app.config import db
import paypalrestsdk
from app.services.orderService import *

from flask import blueprints

paymentbp = blueprints.Blueprint('paymentbp', __name__)


@paymentbp.route('/create-payment', methods=['POST'])
@token_required
@role_required('user')
def create_payment(current_user):
    data = request.json
    full_price = data.get('full_price')
    order_id = data.get('order_id')

    tickets_data = data.get('tickets', [])

    items = []
    for ticket in tickets_data:
        items.append({
            "name": f"Flight {ticket.get('flight_id')} - {ticket.get('ticket_class')}",
            "sku": str(ticket.get('ticket_id')),
            "price": str(ticket.get('price')),
            "currency": "PLN", 
            "quantity": 1
        })

    # Stwórz obiekt płatności PayPal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for('paymentbp.execute_payment', order_id=order_id, _external=True),
            "cancel_url": url_for('paymentbp.payment_cancelled', order_id=order_id, full_price = full_price, _external=True)
        },
        "transactions": [{
            "item_list": {
                "items": items
            },
            "amount": {
                "total": str(full_price),
                "currency": "PLN"
            }
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return jsonify({"approval_url": approval_url})
    else:
        return jsonify({"error": payment.error}), 400
    

@paymentbp.route('/execute-payment', methods=['GET'])
@token_required
@role_required('user')
def execute_payment():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    order_id = request.args.get('order_id')

    if not order_id:
        return jsonify({"error": "Order ID not provided"}), 400

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):

        order = get_order_by_id(order_id)
        if order:
            order.is_payment_completed = True
            db.session.commit()
        return redirect('http://localhost:5173/success')
    else:
        return jsonify({"error": payment.error}), 400


@paymentbp.route('/payment-cancelled', methods=['GET'])
@token_required
@role_required('user')
def payment_cancelled():
    order_Id = request.args.get('order_id')
    fullPrice = request.args.get('full_price')
    return redirect(f'http://localhost:5173/transferdetails?orderId={order_Id}&fullPrice={fullPrice}')
