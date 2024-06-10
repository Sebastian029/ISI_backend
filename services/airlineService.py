from config import app
from controllers.airlineController import *

@app.route("/airlines", methods=["GET"])
def get_airlines():
    try:
        airlines = get_all_airlines_json()
        return airlines
    except ValueError as e:
        return str(e), 404