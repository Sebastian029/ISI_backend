from flask import jsonify, request, url_for, redirect
from config import app,db
import paypalrestsdk
from datetime import datetime
from services.orderService import *


@app.route('/create-payment', methods=['POST'])
@token_required
@role_required('user')
def create_payment():
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
            "return_url": url_for('execute_payment', order_id=order_id, _external=True),
            "cancel_url": url_for('payment_cancelled', order_id=order_id, _external=True)
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
    

@app.route('/execute-payment', methods=['GET'])
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


@app.route('/payment-cancelled', methods=['GET'])
def payment_cancelled():
    # return jsonify({"success": False, "message": "Payment cancelled"})
    return redirect('http://localhost:5173/cancell')
