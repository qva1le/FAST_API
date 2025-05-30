from typing  import Annotated
from fastapi import Depends, Query, Request, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthServices
from src.utils.db_manager import DBManager


class Pagination(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(5,ge=1, lt=30)]

PaginationDep = Annotated[Pagination, Depends()]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthServices().decode_token(token)
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]

def get_db_manager():
    return DBManager(session_factory=async_session_maker)

async def get_db():
    async with get_db_manager() as db:
        yield db

DBDep = Annotated[DBManager , Depends(get_db)]