from flask import jsonify, request, url_for
from config import app
import paypalrestsdk
from datetime import datetime

@app.route('/create-payment', methods=['POST'])
def create_payment():
    data = request.json

    # Pobierz dane zamówienia z żądania
    user_id = data.get('user_id')
    full_price = data.get('full_price')
    is_payment_completed = data.get('is_payment_completed', False)
    paymentMethod = data.get('paymentMethod')
    orderDate = data.get('orderDate', datetime.now().isoformat())

    # Pobierz bilety z żądania
    tickets_data = data.get('tickets', [])

    items = []
    for ticket in tickets_data:
        items.append({
            "name": f"Flight {ticket.get('flight_id')} - {ticket.get('ticket_class')}",
            "sku": str(ticket.get('ticket_id')),
            "price": str(ticket.get('price')),
            "currency": "USD",  # Zakładamy, że waluta jest USD
            "quantity": 1
        })

    # Stwórz obiekt płatności PayPal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for('execute_payment', _external=True),
            "cancel_url": url_for('payment_cancelled', _external=True)
        },
        "transactions": [{
            "item_list": {
                "items": items
            },
            "amount": {
                "total": str(full_price),
                "currency": "USD"
            },
            "description": f"Order payment for user {user_id}"
        }]
    })

    # Utwórz płatność w PayPal
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

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return jsonify({"success": True})
    else:
        return jsonify({"error": payment.error}), 400
    
@app.route('/payment-cancelled', methods=['GET'])
def payment_cancelled():
    return jsonify({"success": False, "message": "Payment cancelled"})