import jwt
from functools import wraps
from flask import request, jsonify
from config import app
from models import User
from datetime import datetime, timedelta

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'}), 401
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(public_id=data['public_id']).first()
       except jwt.ExpiredSignatureError:
           return jsonify({'message': 'token has expired'}), 401
       except jwt.InvalidTokenError:
           return jsonify({'message': 'token is invalid'}), 401
 
       return f(current_user, *args, **kwargs)
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

def generate_jwt_token(user_id):
    expiration_time = datetime.utcnow() + timedelta(minutes=1)
    
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    
    return token