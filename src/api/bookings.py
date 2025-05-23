from fastapi import HTTPException

from fastapi import FastAPI, Body, Query, APIRouter
from datetime import date

from fastapi.params import Depends

from src.api.dependecies import PaginationDep, DBDep, UserIdDep
from src.models.rooms import RoomsOrm
from src.schemas.bookings import Booking, BookingAdd
from src.models.bookings import BookingsOrm

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("")
async def create_booking(room_id: int, user_id: UserIdDep, date_from: date, date_to: date ,db: DBDep,):
    room = await db.session.get(RoomsOrm, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Номер не найден")
    else:
        room_price_per_day = room.price

    days_count = (date_to - date_from).days
    if days_count < 0:
        raise HTTPException(status_code=400, detail="Неверное количество дней")

    total_price = days_count * room_price_per_day

    booking = BookingsOrm(
        room_id=room_id,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
        price=total_price
    )
    await db.bookings.add(booking)
    await db.commit()

    return {"status": "OK", "room_id": room_id, "date_from": date_from, "date_to": date_to, "total_price": total_price}