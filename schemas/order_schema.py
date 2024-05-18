from pydantic import BaseModel, EmailStr, StringConstraints
from typing_extensions import Annotated


class OrderRegistrationModel(BaseModel):
    full_price: str
    is_payment_completed: bool


