from pydantic import BaseModel
from typing import List
from pydantic import field_validator

class TicketData(BaseModel):
    ticket_id: int

class TicketBuyModel(BaseModel):
    tickets: List[TicketData]
    paymentMethod: str

    @field_validator('paymentMethod')
    def names_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only letters')
        return v
