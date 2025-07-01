from fastapi import HTTPException
from pydantic import EmailStr, BaseModel
from sqlalchemy import select, insert

from src.exceptions import UserIsAlreadyExists, ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import User, UserWithHashedPassword
from sqlalchemy.exc import IntegrityError

class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result  = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)

    async def get_one_user(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result  = await self.session.execute(query)
        try:
            model = result.scalars().one_or_none()
        except IntegrityError:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add_user(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one_or_none()
        except IntegrityError:
            raise UserIsAlreadyExists()
        return self.mapper.map_to_domain_entity(model)