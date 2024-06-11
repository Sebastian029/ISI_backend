from app.config import app, db
from app.services.userService import *
from app.services.airlineService import *
from app.services.planeService import *
from app.services.orderService import *
from app.services.airportService import *
from app.services.ticketService import *
from app.services.flightService import *
from app.services.paymentService import *
from app.services.privilageService import *
from app.services.googleService import *
from app.services.followService import *



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)