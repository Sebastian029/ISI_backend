from models.ticket import Ticket
from controllers.planeController import *
from models.order import Order
from config import db
from datetime import datetime


def register_tickets(plane_id, new_flight):
    plane = get_plane_by_id(plane_id)
    rows_bis = plane.seat_rows_bis
    columns_bis = plane.seat_columns_bis
    rows_eco = plane.seat_rows_eco
    columns_eco = plane.seat_columns_eco

    licznik = 0
    # Register Business Class tickets
    for row in range(licznik, rows_bis ):
        for column in range(0, columns_bis ):
            row_label = str(row)
            new_ticket = Ticket(
                flight_id=new_flight.flight_id,
                price=100.0,
                ticket_class="business",
                row=row_label,
                column=column,
                is_bought=0
            )
            db.session.add(new_ticket)

    # Update licznik to continue from where business class left off
    licznik = rows_bis + 1

    # Register Economy Class tickets
    for row in range(licznik, licznik + rows_eco):
        for column in range(0, columns_eco ):
            row_label = str(row)
            new_ticket = Ticket(
                flight_id=new_flight.flight_id,
                price=50.0,
                ticket_class="economy",
                row=row_label,
                column=column,
                is_bought=0
            )
            db.session.add(new_ticket)

    db.session.commit()
  


def get_ticket(ticket_id):
    return Ticket.query.get(ticket_id)

def get_tickets_id(flightid):
    tickets = db.session.query(
            Ticket
        ).filter(
            Ticket.flight_id == flightid,
        ).all()
    
    json_tickets = []
    for ticket in tickets:
        column_value = ticket.column
        if column_value == 2:
            column_value = 3
        elif column_value == 3:
            column_value = 4
        
        json_ticket = {
            "ticket_id": ticket.ticket_id,
            "flight_id": ticket.flight_id,
            "ticket_class": ticket.ticket_class,
            "is_bought": ticket.is_bought,
            "row": ticket.row,
            "column": column_value,
            "price": ticket.price
        }
        json_tickets.append(json_ticket)

    num_columns = max(ticket.column for ticket in tickets) if tickets else 0
    total_seats = len(tickets)
    
    result = {
        "tickets": json_tickets,
        "num_columns": num_columns,
        "total_seats": total_seats
    }
    
    return result



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