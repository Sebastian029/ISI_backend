from config import app, db
from services.userService import *
from services.airlineService import *
from services.planeService import *
from services.orderService import *
from services.airportService import *
from services.ticketService import *
from services.flightService import *
from services.paymentService import *
from services.privilageService import *
from services.googleService import *
from services.followService import *

@app.route("/")
def init():
    return "Hello WORLD"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)