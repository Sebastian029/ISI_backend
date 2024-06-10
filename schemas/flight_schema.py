from pydantic import BaseModel, field_validator
from datetime import datetime
import re

class FlightRegisterSchema(BaseModel):
    departure_airport_id: int
    arrive_airport_id: int
    travel_time: str
    distance: float 
    plane_id: int
    airline_id: int
    data_lotu: str

    @field_validator('distance')
    def distance_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Distance must be a positive number')
        return v

    @field_validator('travel_time')
    def travel_time_format(cls, v):
        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError('Travel time must be in the format HH:MM')
        # Optional: Add more validation to ensure HH is 00-23 and MM is 00-59
        hours, minutes = map(int, v.split(':'))
        if not (0 <= hours <= 23) or not (0 <= minutes <= 59):
            raise ValueError('Travel time must be a valid time in HH:MM format')
        return v

    @field_validator('data_lotu')
    def flight_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in the format YYYY-MM-DD')
        return v
    
class FlightSearchSchema(BaseModel):
    departure_airport_id: int
    arrive_airport_id: int
    data_lotu: str

    @field_validator('data_lotu')
    def flight_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in the format YYYY-MM-DD')
        return v
    
class FlightSearchSchemaWithoutDate(BaseModel):
    departure_airport_id: int
    arrive_airport_id: int