from pydantic import BaseModel, EmailStr, StringConstraints,Field
from typing_extensions import Annotated
from typing import Optional
from pydantic import field_validator

class UserRegistrationModel(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phoneNumber: Annotated[str, StringConstraints(min_length=9, max_length=9)]
    password: str

    @field_validator('firstName', 'lastName')
    def names_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only letters')
        return v

class UserUpdateModel(BaseModel):  
    phoneNumber: Optional[str] = Field(None, min_length=9, max_length=9)
    name: Optional[str] = None
    surname: Optional[str] = None

    @field_validator('name', 'surname')
    def names_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only letters')
        return v

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

class UserSearchModel(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @field_validator('name', 'surname')
    def names_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only letters')
        return v

class UserModel(BaseModel):
    firstName: str
    lastName: str

    @field_validator('firstName', 'lastName')
    def names_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only letters')
        return v