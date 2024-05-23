from models.ticket import Ticket
from controllers.planeController import *
from models.order import Order
from config import db
from datetime import datetime


def register_tickets_bis(plane_id, new_flight):
   
    plane = get_plane_by_id(plane_id)
    rows_bis = plane.seat_rows_bis
    columns_bis = plane.seat_columns_bis

    for row in range(1, rows_bis + 1):
        for column in range(1, columns_bis + 1):
            row_label =chr(ord('A') + row - 1) + chr(ord('A') + row - 1)  
            new_ticket = Ticket(flight_id=new_flight.flight_id,
                                price=100.0,  
                                ticket_class="Business",  
                                row=row_label,
                                column=column,
                                is_bought=0)
            db.session.add(new_ticket)
    
    db.session.commit()


def register_tickets_eco(plane_id, new_flight):
  
    plane = get_plane_by_id(plane_id)
    rows_eco = plane.seat_rows_eco
    columns_eco = plane.seat_columns_eco

    for row in range(1, rows_eco + 1):
        for column in range(1, columns_eco + 1):
            row_label = chr(ord('A') + row - 1) 
            new_ticket = Ticket(flight_id=new_flight.flight_id,
                                price=50.0,  
                                ticket_class="Economy",  
                                row=row_label,
                                column=column,
                                is_bought=0)
            db.session.add(new_ticket)

    db.session.commit()
  


def get_ticket(ticket_id):
    return Ticket.query.get(ticket_id)

def get_tickets_id(flightid):
    tickets = db.session.query(
            Ticket
        ).filter(
            Ticket.flight_id == flightid,
            Ticket.is_bought == 0
        ).all()
    
    json_tickets = [
        {
            "ticket_id":ticket.ticket_id,
            "flight_id":ticket.flight_id,
            "ticket_class": ticket.ticket_class,
            "row": ticket.row,
            "column": ticket.column,
            "price": ticket.price
        }
        for ticket in tickets
    ]
    return json_tickets

def buy_tickets_service(current_user, ticket_ids,paymentMethod):
    if not ticket_ids:
        return {"message": "No tickets provided in the request body"}, 400

    try:
        new_order = Order(user_id = current_user.user_id, full_price = 0, is_payment_completed = 0, paymentMethod = paymentMethod, orderDate = datetime.now() )
        db.session.add(new_order)

        total_price = 0

        for ticket_id in ticket_ids:
            ticket = get_ticket(ticket_id)

            if ticket:
                ticket_price = ticket.price  
                ticket.is_bought = True
                ticket.order_id = new_order.order_id
                total_price += ticket_price
            else:
                db.session.rollback()
                return {"message": f"Ticket with id {ticket_id} not found"}, 404

        new_order.full_price = total_price

        db.session.commit()
        return {"message": "Tickets successfully marked as bought", "order_id": new_order.order_id, "full_price": new_order.full_price}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500
    
def delete_ticket_service(ticket_id):
    try:
        ticket = get_ticket(ticket_id)
        if ticket:
            if ticket.is_bought == 0:  
                db.session.delete(ticket)
                db.session.commit()
                return {"message": "Bilet został usunięty pomyślnie."}, 200
            else:
                return {"message": "Nie można usunąć biletu, który został już kupiony."}, 400
        else:
            return {"message": "Nie znaleziono biletu o podanym ID."}, 404
    except Exception as e:
        db.session.rollback()
        return {"message": "Wystąpił błąd podczas usuwania biletu: " + str(e)}, 400
    
def update_ticket_price_service(ticket_id, new_price):
    try:
        if not new_price:
            return {"message": "Nie podano nowej ceny biletu."}, 400

        ticket = get_ticket(ticket_id)
        if ticket:
            ticket.price = new_price
            db.session.commit()
            return {"message": "Cena biletu została zaktualizowana pomyślnie."}, 200
        else:
            return {"message": "Nie znaleziono biletu o podanym ID."}, 404
    except Exception as e:
        db.session.rollback()
        return {"message": "Wystąpił błąd podczas aktualizowania ceny biletu: " + str(e)}, 400