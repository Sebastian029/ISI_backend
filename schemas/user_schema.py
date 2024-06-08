from pydantic import BaseModel, EmailStr, StringConstraints,Field
from typing_extensions import Annotated
from typing import Optional

class UserRegistrationModel(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phoneNumber: Annotated[str, StringConstraints(min_length=9, max_length=9)]
    password: str

class UserUpdateModel(BaseModel):  
    phoneNumber: Optional[str] = Field(None, min_length=9, max_length=9)
    name: Optional[str] = None
    surname: Optional[str] = None

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

class UserSearchModel(BaseModel):
    name: str
    surname: str
    email: EmailStr

class UserModel(BaseModel):
    firstName: str
    lastName: str