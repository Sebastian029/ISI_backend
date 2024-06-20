from flask import request,redirect,json
from app.controllers.userController import *
from app.utils import *
from oauthlib.oauth2 import WebApplicationClient
import requests
from app.controllers.roleUserController import create_user
from app.controllers.tokenController import get_first_free_token_id

from flask import blueprints

googlebp = blueprints.Blueprint('googlebp', __name__)

GOOGLE_CLIENT_ID = '211513266277-n9ahn4rsqgnsdo6330roufqp3uev8lt3.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()



@googlebp.route("/login/google", methods=['GET', 'POST'])
def login_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@googlebp.route("/login/google/callback", methods=['GET', 'POST'])
def callback():
    code = request.args.get("code")

    if not code:
        return redirect("http://localhost:5173/")

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
        user = create_user(
            firstName=users_name,
            lastName=users_lastname,
            phone_number=None,
            email=users_email,
            password="*",
        )
    access_token = generate_access_token(user.public_id, ['user'], user.name, user.surname)
    refresh_token = generate_refresh_token(user.public_id, ['user'], user.name, user.surname)

    token = Token(token_id = get_first_free_token_id(), refresh_token = refresh_token, access_token = access_token, user_id = user.user_id )
    db.session.add(token)
    db.session.commit()

    return redirect(f"http://localhost:5173/?access_token={access_token}&refresh_token={refresh_token}")