from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import paypalrestsdk
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
import os 



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})


app.config['SECRET_KEY']='daaa9975582b77c920be486c44667846'
app.config['ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=30)
app.config['REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

app.config['BLACKLIST'] = set()

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://avnadmin:AVNS_vOiMluD6tv7HMw07Ho7@mysql-27dba8ad-cichywojxpompa-acd5.b.aivencloud.com:23900/defaultdb?ssl_ca=ssl_cert.pem'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  

paypalrestsdk.configure({
    "mode": "sandbox", 
    "client_id": "AfCyxkusZA2IM5tG9K78TGlYjlMlzsKQ7G_nRP2S2BMn_920Sy8n6k7NbhsrpmpTGs14J6ECG6G4-W71",
    "client_secret": "EGTY4q16PVR4-y9EsdAojoLruHVM7YxsI-CQvFSpvtwdOhOPBJkVI8yMg4GEZjaBnjZxNS8G2mPi8YAT"
})



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'