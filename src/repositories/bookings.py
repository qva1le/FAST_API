from datetime import date
from distutils.util import execute

from fastapi import HTTPException
from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Booking, BookingAdd


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

    # async def add_booking(self, date_from, date_to, hotel_id, room_id):
    #     rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
    #     result = await self.session.execute(rooms_ids_to_get)
    #     rooms_ids_to_get = []
    #     for row in result.fetchall():
    #         rooms_ids_to_get.append(row[0])
    #
    #     if room_id not in rooms_ids_to_get:
    #         raise HTTPException(status_code=409, detail="Больше таких номеров нету")

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        #получаем свободные номера(айди номеров) по датам
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        #выполняем запрос к базе
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        #получаем данные(айди номеров) в виде списка, scalars - первая столбик, all - все айдишники
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()
        #проверка есть ли room_id в доступных номерах
        if data.room_id in rooms_ids_to_book:
            #если есть создаём бронирование
            new_booking = await self.add(data)
            #возвращаем бронь
            return new_booking
        else:
            #иначе ошибка
            raise HTTPException(500)











