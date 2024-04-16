from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://avnadmin:AVNS_vOiMluD6tv7HMw07Ho7@mysql-27dba8ad-cichywojxpompa-acd5.b.aivencloud.com:23900/defaultdb?ssl_ca=ssl_cert.pem'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
