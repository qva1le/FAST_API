from fastapi import APIRouter, HTTPException, Response

from src.api.dependecies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthServices

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    existing_user = await db.users.get_one_or_none(email=data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")

    hashed_password = AuthServices().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
    return {"status": "OK"}

@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
        user = await db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthServices().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthServices().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
        return await db.users.get_one_or_none(id=user_id)


@router.get("/logout")
async def logout_user(response: Response):
        response.delete_cookie("access_token")
        return {"status": "OK"}