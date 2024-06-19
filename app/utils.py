import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.models.user import User
from datetime import datetime, timedelta
from app.models.refreshtoken import RefreshToken
from app.config import db

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
        if not token:
           return jsonify({'message': 'a valid token is missing'}), 401
       
        if token in current_app.config['BLACKLIST']:
           return jsonify({'message': 'token is blacklisted'}), 401

        try:
           data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(public_id=data['public_id']).first()
        except jwt.ExpiredSignatureError:
           return jsonify({'message': 'token has expired'}), 401
        except jwt.InvalidTokenError:
           return jsonify({'message': 'token is invalid'}), 401
 
        return f(current_user, *args, **kwargs)
   return decorator

def generate_access_token(public_id):
    payload = {
        'exp': datetime.utcnow() + current_app.config['ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.utcnow(),
        'public_id': public_id
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def generate_refresh_token(public_id):
    payload = {
        'exp': datetime.utcnow() + current_app.config['REFRESH_TOKEN_EXPIRES'],
        'iat': datetime.utcnow(),
        'public_id': public_id
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    refresh_token = RefreshToken(
        token=token,
        public_id=public_id,
        expires=datetime.utcnow() + current_app.config['REFRESH_TOKEN_EXPIRES'],
        revoked=0
    )
    db.session.add(refresh_token)
    db.session.commit()
    return token

def revoke_token(token, secondToken):
    refresh_token = RefreshToken.query.filter_by(token=token).first()
    current_app.config['BLACKLIST'].add(secondToken)
    if refresh_token:
        refresh_token.revoked = True
        db.session.commit()
        return True
    return False

# def decode_token(token):
#     try:
#         payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#         return payload['sub']
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None

def privilege_required(privilege_name):
    def decorator(func):
        @wraps(func)
        def authorize(current_user, *args, **kwargs):
            privileges = current_user.privileges
            list_privileges = [privilege.name for privilege in privileges]
            if privilege_name not in list_privileges:
                return jsonify({'message': 'privilege is invalid'}), 403
            return func(current_user, *args, **kwargs)
        return authorize
    return decorator

def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def authorize(current_user, *args, **kwargs):
            roles = current_user.roles
            list_roles = [role.name for role in roles]
            if role_name not in list_roles:
                return jsonify({'message': 'role is invalid'})
            return func(current_user, *args, **kwargs)
        return authorize
    return decorator





# def generate_jwt_token(public_id):
#     expiration_time = datetime.utcnow() + timedelta(minutes=15)
    
#     payload = {
#         'public_id': public_id,
#         'exp': expiration_time
#     }
    
#     token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    
#     return token