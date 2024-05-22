from pydantic import BaseModel
from typing import List

class TicketData(BaseModel):
    ticket_id: int

class TicketBuyModel(BaseModel):
    tickets: List[TicketData]
    paymentMethod: str
