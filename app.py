from flask import Flask
from config import app, db
from order_routes import *
from other_routes import get_flights_with_airports
from user_routes import *
from airport import get_ports
from plane import get_planes
from airline import get_airlines

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)