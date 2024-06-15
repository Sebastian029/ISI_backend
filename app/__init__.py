from flask import Flask
from datetime import timedelta
from flask_cors import CORS
from .config import db,mail
from .services.userService import userbp
from .services.ticketService import ticketbp
from .services.privilageService import privilagebp
from .services.planeService import planebp
from .services.paymentService import paymentbp
from .services.orderService import orderbp
from .services.googleService import googlebp
from .services.followService import followbp
from .services.flightService import fligtbp
from .services.airportService import airportbp
from .services.airlineService import airlinebp


def create_app(database_uri="mysql://avnadmin:AVNS_vOiMluD6tv7HMw07Ho7@mysql-27dba8ad-cichywojxpompa-acd5.b.aivencloud.com:23900/defaultdb?ssl_ca=ssl_cert.pem"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config['SECRET_KEY']='daaa9975582b77c920be486c44667846'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
    app.config['REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    app.config['BLACKLIST'] = set()
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5000"]}})
    app.config['MAIL_SERVER']='smtp.fastmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'dominikjaroszek@fastmail.com'
    app.config['MAIL_PASSWORD'] = '8a869t468s522z3x'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    app.register_blueprint(userbp)
    app.register_blueprint(ticketbp)
    app.register_blueprint(privilagebp)
    app.register_blueprint(planebp)
    app.register_blueprint(paymentbp)
    app.register_blueprint(orderbp)
    app.register_blueprint(googlebp)
    app.register_blueprint(followbp)
    app.register_blueprint(fligtbp)
    app.register_blueprint(airportbp)
    app.register_blueprint(airlinebp)
    



    db.init_app(app)
    mail.init_app(app)
    return app