from flask import jsonify, request
from app.utils import token_required, role_required
from app.controllers.followController import *
from app.controllers.airlineController import get_airline_by_id
from app.controllers.airportController import get_airports_by_id
from app.controllers.planeController import get_plane_by_id
from pydantic import ValidationError
from app.controllers.flightController import get_flight_by_id

from flask import blueprints

followbp = blueprints.Blueprint('followbp', __name__)

@followbp.route("/follow", methods=["POST"])
@token_required
@role_required('user')
def follow(current_user):
    try:
        data = request.get_json()
        flight_id = data.get('flight_id')
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    if not flight_id:
        return jsonify({"message": "flight_id parameter is required"}), 400

    if not (get_flight_by_id(flight_id)):
        return jsonify({"message": "Wystąpił błąd, nie ma takiego flight_id"}), 400

    if (get_follow(current_user.user_id, flight_id)):
        return jsonify({"message": "Już obserwujesz tego użytkownika"}), 400

    try:
        follow = create_follow(user_id=current_user.user_id, flight_id=flight_id)
        return jsonify({"message": "Użytkownik obserwuje lot!", "follow_id": follow.follow_id}), 201
    except Exception as e:
        return jsonify({"message": "Wystąpił błąd przy dodawaniu obserwacji do bazy danych: " + str(e)}), 400
    

@followbp.route("/unfollow/<int:follow_id>", methods=["DELETE"])
@token_required
@role_required('user')
def unfollow(current_user, follow_id):

    if delete_follow(follow_id):
            return jsonify({"message": "Follow deleted!"}), 200
    else:
            return jsonify({"message": "Follow not found"}), 404
    
@followbp.route("/follows", methods=["GET"])
@token_required
@role_required('user')
def get_follows(current_user):
    follows = get_follows_by_user_id(current_user.user_id)
    follow_flight_data = []

    for follow in follows:
        flight = get_flight_by_id(follow.flight_id)
        if flight:
            departure_airport = get_airports_by_id(flight.departure_airport_id)
            arrive_airport = get_airports_by_id(flight.arrive_airport_id)
            plane = get_plane_by_id(flight.plane_id)
            airline = get_airline_by_id(flight.airline_id)
            is_follow = get_follow(current_user.user_id, flight.flight_id)
            follow_flight_data.append({
                "flight_id": flight.flight_id,
                "departure_airport": departure_airport.Airport.airport_name if departure_airport else None,
                "arrival_airport": arrive_airport.Airport.airport_name if arrive_airport else None,
                "departure_city": departure_airport.city_name if departure_airport else None,
                "arrival_city": arrive_airport.city_name if arrive_airport else None,
                "travel_time": str(flight.travel_time),
                "distance": flight.distance,
                "available_seats": flight.available_seats,
                "plane_name": plane.plane_name if plane else None,
                "airline_name": airline.airline_name if airline else None,
                "data_lotu": flight.data_lotu,
                "is_follow": bool(is_follow),
                "follow_id":is_follow.follow_id if is_follow else None
            })
        else:
            flight_info = None

      
    return jsonify(follow_flight_data), 200