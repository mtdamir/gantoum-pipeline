import logging
from fastapi import HTTPException
from db.create_user_table import create_user, get_user_by_phone_number, update_user_refresh_token
from schemas.user_schema import UserSchema, Roles
from dtos.auth_dto import RegisterUserDto, LoginUserDto
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from config.settings import settings
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire_minutes = timedelta(minutes=30)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def register_user(self, register_user: RegisterUserDto) -> UserSchema:
        name = register_user.username
        email = register_user.email
        password = register_user.password
        phone_number = register_user.phone_number

        existing_user = await get_user_by_phone_number(phone_number)
        if existing_user:
            raise HTTPException(status_code=400, detail="This user already registered")

        password_hash = self.get_password_hash(password)

        created_user = await create_user(
            name=name,
            email=email,
            phone_number=phone_number,
            password_hash=password_hash,
            role=Roles.USER.value
        )

        return UserSchema(
            name=created_user["name"],
            email=created_user["email"],
            phone_number=created_user["phone_number"],
            role=created_user["role"],
            created_at=created_user["created_at"]
        )

    async def login_user(self, login_user: LoginUserDto) -> dict:
        phone_number = login_user.phone_number

        user = await get_user_by_phone_number(phone_number)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        if not self.verify_password(login_user.password, user["password_hash"]):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token_expires = timedelta(minutes=30)
        access_token = self.create_access_token(data={"user_id": user["user_id"], "role": user["role"]}, expires_delta=access_token_expires)
        
        refresh_token_expires = timedelta(days=7)
        refresh_token = self.create_access_token(data={"user_id": user["user_id"], "role": user["role"]}, expires_delta=refresh_token_expires)

        await update_user_refresh_token(user["email"], refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }