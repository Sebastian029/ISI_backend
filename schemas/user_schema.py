from pydantic import BaseModel, EmailStr, StringConstraints
from typing_extensions import Annotated


class UserRegistrationModel(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phoneNumber: Annotated[str, StringConstraints(min_length=9, max_length=9)]
    password: str

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
