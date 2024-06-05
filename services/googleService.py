from flask import request, jsonify ,redirect,json
from config import app, db
from controllers.userController import *
from controllers.roleUserController import *
from controllers.roleController import all_get_role
from utils import *
from oauthlib.oauth2 import WebApplicationClient
import requests

GOOGLE_CLIENT_ID = '211513266277-n9ahn4rsqgnsdo6330roufqp3uev8lt3.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()



@app.route("/login/google", methods=['GET', 'POST'])
def login_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/google/callback", methods=['GET', 'POST'])
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        users_lastname = userinfo_response.json()["family_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = get_user_by_email(users_email)
    if not user:
        # Create new user
        user = User(
            name=users_name,
            surname=users_lastname,
            phone_number="",
            email=users_email,
            password="password"
        )
        db.session.add(user)
        db.session.commit()

    # Generate tokens
    access_token = generate_access_token(user.public_id)
    refresh_token = generate_refresh_token(user.public_id)

    # Redirect to React app with tokens
    rola = "user"
    return redirect(f"http://localhost:5173/?access_token={access_token}&refresh_token={refresh_token}&roles={rola}")