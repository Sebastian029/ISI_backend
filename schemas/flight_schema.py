from pydantic import BaseModel, field_validator

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
        return v

    @field_validator('data_lotu')
    def flight_date_format(cls, v):
        return v
    
class FlightSearchSchema(BaseModel):
    departure_airport_id: int
    arrive_airport_id: int
    data_lotu: str

    @field_validator('data_lotu')
    def flight_date_format(cls, v):
        # Dodaj tutaj logikę walidacji formatu daty lotu, np. sprawdzając czy jest w formacie YYYY-MM-DD
        return v
    
class FlightSearchSchemaWithoutDate(BaseModel):
    departure_airport_id: int
    arrive_airport_id: int