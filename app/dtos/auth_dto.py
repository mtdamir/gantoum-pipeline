from pydantic import BaseModel , Field
from typing import Optional

class RegisterUserDto(BaseModel):
    username: str
    email: str
    password: str = Field(..., min_length=8)
    phone_number: str 


class LoginUserDto(BaseModel):
    username: str
    password: str = Field(..., min_length=8)
    phone_number: str 