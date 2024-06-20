from app.controllers.userController import get_user_by_id
from app.models.ticket import Ticket
from app.controllers.planeController import *
from app.controllers.flightController import update_available_seats, get_flight_by_id
from app.models.order import Order
from app.config import db
from datetime import datetime
from flask_mailman import EmailMessage


def register_tickets(plane_id, new_flight):
    plane = get_plane_by_id(plane_id)
    rows_bis = plane.seat_rows_bis
    columns_bis = plane.seat_columns_bis
    rows_eco = plane.seat_rows_eco
    columns_eco = plane.seat_columns_eco

    licznik = 0
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

    licznik = rows_bis + 1

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
  


def get_ticket_by_id(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket with id {ticket_id} not found")
    return ticket

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



def buy_tickets_service(current_user, ticket_ids, paymentMethod):
    if not ticket_ids:
        return {"message": "No tickets provided in the request body"}, 400

    try:
        # Check if any of the tickets are already bought
        already_bought_tickets = []
        for ticket_id in ticket_ids:
            ticket = get_ticket_by_id(ticket_id)
            if not ticket:
                return {"message": f"Ticket with id {ticket_id} not found"}, 404
            if ticket.is_bought:
                already_bought_tickets.append(ticket_id)

        if already_bought_tickets:
            return {"message": f"Tickets with ids {already_bought_tickets} are already bought"}, 400

        new_order = Order(user_id=current_user.user_id, full_price=0, is_payment_completed=0, paymentMethod=paymentMethod, orderDate=datetime.now())
        db.session.add(new_order)

        total_price = 0
        remaining_tickets = len(ticket_ids)
        update_available_seats(ticket.flight_id, remaining_tickets)
        flight_id = None
        for ticket_id in ticket_ids:
            ticket = get_ticket_by_id(ticket_id)
            if ticket:
                ticket_price = ticket.price
                ticket.is_bought = True
                ticket.order_id = new_order.order_id
                total_price += ticket_price
                flight_id = ticket.flight_id
            else:
                db.session.rollback()
                return {"message": f"Ticket with id {ticket_id} not found"}, 404

        new_order.full_price = total_price
        db.session.commit()
        send_order_email(current_user.user_id, flight_id)

        return {"message": "Tickets successfully marked as bought", "order_id": new_order.order_id, "full_price": new_order.full_price}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500
    

def send_order_email(user_id, flight_id):
    try:
        user = get_user_by_id(user_id)
        flight = get_flight_by_id(flight_id)
        email = user.email
        if user and flight:
            msg = EmailMessage(
                'Hi ' + str(user.name) + '! ',
                'Thank you for choosing us! \n' +
                'Your reservation for the flight fom: ' + str(flight.departure_airport.airport_name) + ' to '
                + str(flight.arrive_airport.airport_name) + ' has ben successfully made \n'
                'Date of your flight: ' + str(flight.data_lotu),
                'dominikjaroszek@fastmail.com',
                [str(email)],
            )
            msg.send()
            return "Email sent"
    except Exception as e:
        return str(e)


def delete_ticket_service(ticket_id):
    try:
        ticket = get_ticket_by_id(ticket_id)
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

        ticket = get_ticket_by_id(ticket_id)
        if ticket:
            ticket.price = new_price
            db.session.commit()
            return {"message": "Cena biletu została zaktualizowana pomyślnie."}, 200
        else:
            return {"message": "Nie znaleziono biletu o podanym ID."}, 404
    except Exception as e:
        db.session.rollback()
        return {"message": "Wystąpił błąd podczas aktualizowania ceny biletu: " + str(e)}, 400