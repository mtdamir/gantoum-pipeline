from pydantic import BaseModel, Field, EmailStr, model_validator
from fastapi import HTTPException
from typing import Optional
from datetime import datetime, timezone
from enums.user_enums import Roles

class UserSchema(BaseModel):
    user_id: Optional[int] = None
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Roles = Roles.USER.value
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    refresh_token: Optional[str] = None

    @model_validator(mode="after")
    def validate_user(cls, values):
        values["updated_at"] = datetime.now(timezone.utc)
        if values["role"] not in Roles.__members__:
            raise HTTPException(status_code=400, detail="Invalid role.")
        return values

    class Config:
        schema_extra = {
            "example": {
                "name": "Ali Rezaei",
                "email": "user@example.com",
                "password": "yoursecurepassword",
                "role": "user"
            }
        }