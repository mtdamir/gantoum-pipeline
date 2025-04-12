from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException
from typing import Optional
from datetime import datetime
from enums.user_enums import Roles

class UserSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    role: Roles = Field(default=Roles.USER.value)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    refresh_token: str = Field(default=None, nullable = True)

    @classmethod
    def validate_user(cls, data):
        if "created_at" not in data or data["created_at"] is None:
            data["created_at"] = datetime.timezone.utc()

        data["updated_at"] = datetime.timezone.utc()

        if data["role"] not in [role.value for role in Roles]:
            raise HTTPException(status_code=400, detail=["Invalid role."])

        
        if data.get(  "refresh_token") is None:
            data.pop("refresh_token", None)
        return cls(**data)

    class Config:
        schema_extra = {
            "example": {
                "phone_number": "09120001122",
                "email": "user@example.com",
                "password": "yoursecurepassword",
                "is_verified": False,
                "role": "user"
            }
        }



