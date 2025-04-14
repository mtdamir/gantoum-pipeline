from fastapi import APIRouter
from service.user_service import UserService
from dtos.auth_dto import RegisterUserDto, LoginUserDto

router = APIRouter()
auth_service = UserService()


@router.post("/register")
async def register_user(register_user: RegisterUserDto):    
    return await auth_service.register_user(register_user)


@router.post("/login")
async def login_user(login_user: LoginUserDto):
    return await auth_service.login_user(login_user)