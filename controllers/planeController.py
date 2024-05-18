from models.plane import Plane
from config import db

def get_plane_by_id(id):
    return Plane.query.get(id)

def get_all_planes_json():
    planes = Plane.query.all()
    if not planes:
        return []
    planes = [plane.to_json() for plane in planes]
    return planes

def available_seat(id):
    plane = get_plane_by_id(id)
    return plane.seat_rows_bis*plane.seat_columns_bis + plane.seat_rows_eco*plane.seat_columns_eco

