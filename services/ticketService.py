from config import app, db
from controllers.ticketController import  *
from controllers.orderController import *
from flask import request, jsonify
from utils import token_required,role_required,privilege_required
from schemas.ticket_schema import TicketBuyModel
from pydantic import ValidationError

@app.route("/tickets/<int:flightid>", methods=["GET"])
def get_tickets(flightid):
    try:
        tickets = get_tickets_id(flightid)
        return jsonify(tickets)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/ticket_buy", methods=["POST"])
@token_required
@role_required('user')
# @privilege_required('buying')
def buy_tickets(current_user):
    try:
        data = request.json
        tickets_to_buy = TicketBuyModel(**data)
        ticket_ids = [ticket.ticket_id for ticket in tickets_to_buy.tickets]
        response, status_code = buy_tickets_service(current_user, ticket_ids)
        return jsonify(response), status_code
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route("/delete_ticket/<int:ticket_id>", methods=["DELETE"])
@token_required
@role_required('admin')
def delete_ticket(current_user, ticket_id):
    result, status_code = delete_ticket_service(ticket_id)
    return jsonify(result), status_code
    

@app.route("/update_ticket_price/<int:ticket_id>", methods=["PATCH"])
@token_required
@role_required('admin')
def update_ticket_price(current_user, ticket_id):
    try:
        data = request.json
        new_price = data.get("new_price")
        result, status_code = update_ticket_price_service(ticket_id, new_price)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"message": "Wystąpił błąd podczas przetwarzania żądania: " + str(e)}), 500