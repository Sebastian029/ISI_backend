from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://avnadmin:AVNS_8CrfzEXBKXeI0JsTIiI@mysql-3d129384-projekt-e473.a.aivencloud.com:15644/defaultdb?ssl_ca=ssl_cert.pem'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)