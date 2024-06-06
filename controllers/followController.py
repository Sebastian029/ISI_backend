from models.follow import Follow
from config import db
from flask import jsonify

def create_follow(user_id, flight_id):
    new_follow = Follow(user_id=user_id, flight_id=flight_id)
    
    db.session.add(new_follow)
    db.session.commit()
    return new_follow

def get_follow(user_id, flight_id):
    follow = Follow.query.filter_by(user_id=user_id, flight_id=flight_id).first()
    if not follow:
        return False
    return follow

def get_follow_by_id(follow_id):
    return Follow.query.get(follow_id)

def delete_follow(follow_id):
    follow = Follow.query.get(follow_id)
    if not follow:
        return False
    db.session.delete(follow)
    db.session.commit()
    return True

def get_follows_by_user_id(user_id):
    return Follow.query.filter_by(user_id=user_id).all()