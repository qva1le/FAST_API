from datetime import date
from distutils.util import execute

from fastapi import HTTPException
from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, date_from, date_to, hotel_id, room_id):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        result = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_get = []
        for row in result.fetchall():
            rooms_ids_to_get.append(row[0])

        if room_id not in rooms_ids_to_get:
            raise HTTPException(status_code=409, detail="Больше таких номеров нету")









