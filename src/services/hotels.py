from datetime import date

from fastapi import HTTPException

from src.exceptions import DatesAreIncorrect, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelService (BaseService):
    async def get__filtered_by_time(
            self,
            pagination,
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date,
    ):
        if date_from >= date_to:
            raise HTTPException(status_code=409, detail=DatesAreIncorrect.detail)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one_or_none(id=hotel_id)

    async def add_hotel(self,hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def get_hotel_with_check(self, hotel_id: int) -> None:
        try:
            return await self.db.hotels.get_one(hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException