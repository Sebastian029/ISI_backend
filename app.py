from flask import Flask
from config import app, db
from order_routes import *
# from other_routes import *
from user_routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)