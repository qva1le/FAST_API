from fastapi import APIRouter, HTTPException, Response
from starlette.responses import RedirectResponse

from src.api.dependecies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthServices

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    hashed_password = AuthServices().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthServices().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthServices().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.get("/me")
async def get_me(
        user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.get("/logout")
async def logout_user(
    user_id: UserIdDep,
    response: Response,
):
    async with async_session_maker() as session:
        response = RedirectResponse('/login', status_code=302)
        response.delete_cookie("access_token")
        return response