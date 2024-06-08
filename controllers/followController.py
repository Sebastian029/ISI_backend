from models.follow import Follow
from config import db
from flask import jsonify

def get_first_free_follow_id():
    all_follow_ids = db.session.query(Follow.follow_id).order_by(Follow.follow_id).all()
    all_follow_ids = [row.follow_id for row in all_follow_ids]
    
    # Szukamy pierwszego brakującego ID
    for index in range(1, len(all_follow_ids) + 1):
        if index not in all_follow_ids:
            return index
    
    return len(all_follow_ids) + 1

def create_follow(user_id, flight_id):
    new_follow_id = get_first_free_follow_id()

    follow = Follow(
        follow_id=new_follow_id,
        user_id=user_id,
        flight_id=flight_id
    )

    db.session.add(follow)
    db.session.commit()
    return follow

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

