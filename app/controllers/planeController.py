from app.models.plane import Plane
from app.config import db

def get_plane_by_id(id):
    plane = Plane.query.get(id)
    if not plane:
        raise ValueError(f"Plane with id {id} not found")
    return plane

def get_all_planes_json():
    planes = Plane.query.all()
    if not planes:
        raise ValueError(f"Planes not found")
    planes = [plane.to_json() for plane in planes]
    return planes

def available_seat(id):
    plane = get_plane_by_id(id)
    return plane.seat_rows_bis*plane.seat_columns_bis + plane.seat_rows_eco*plane.seat_columns_eco

