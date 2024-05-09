from config import app, db
from models import  Ticket,Order
from flask import request, jsonify
from utils import token_required,role_required

@app.route("/tickets", methods=["GET"])
def get_tickets():
    try:
        flightid = request.args.get("flightId")

        tickets = db.session.query(
            Ticket
        ).filter(
            Ticket.flight_id == flightid,
            Ticket.is_bought == 0
        ).all()

        json_tickets = [
            {
                "ticket_id":ticket.ticket_id,
                "ticket_class": ticket.ticket_class,
                "row": ticket.row,
                "column": ticket.column,
                "price": ticket.price
            }
            for ticket in tickets
        ]

        return jsonify(json_tickets)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/ticket_buy", methods=["POST"])
@token_required
@role_required('user')
def buy_tickets(current_user):
    data = request.json
    tickets_to_buy = data.get("tickets")

    if not tickets_to_buy:
        return jsonify({"message": "No tickets provided in the request body"}), 400

    try:
        new_order = Order(user_id=current_user.user_id, full_price=0, is_payment_completed=0)
        db.session.add(new_order)

        total_price = 0

        for ticket_data in tickets_to_buy:
            ticket_id = ticket_data.get("ticket_id")
            
            ticket = Ticket.query.get(ticket_id)

            if ticket:
                ticket_price = ticket.price  
                ticket.is_bought = True
                ticket.order_id = new_order.order_id
                total_price += ticket_price
            else:
                db.session.rollback()
                return jsonify({"message": f"Ticket with id {ticket_id} not found"}), 404

        new_order.full_price = total_price

        db.session.commit()
        return jsonify({"message": "Tickets successfully marked as bought", "order_id": new_order.order_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
