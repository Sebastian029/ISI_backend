from config import app, db
from models import  Ticket
from flask import request, jsonify


@app.route("/tickets", methods=["GET"])
def get_tickets():
    try:
        flightid = request.args.get("flightId")

        tickets = db.session.query(
            Ticket
        ).filter(
            Ticket.flight_id == flightid,
            Ticket.is_bought == 1
        ).all()

        json_tickets = [
            {
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