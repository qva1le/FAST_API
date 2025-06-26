from fastapi import HTTPException

from fastapi import FastAPI, Body, Query, APIRouter
from datetime import date

from fastapi.params import Depends

from src.api.dependecies import PaginationDep, DBDep, UserIdDep
from src.models.rooms import RoomsOrm
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest
from src.models.bookings import BookingsOrm

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get("")
async def get_bookings(
        db: DBDep,
        room_id: int | None =Query(None, description="Айдишник номера"),
):
    if room_id is None:
        return await db.bookings.get_all(room_id=room_id)
    else:
        return await db.bookings.get_filtered(room_id=room_id)


@router.get("/me")
async def get_me_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)

@router.post("")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.delete("/{bookings_id}")
async def delete_bookings(booking_id: int, db: DBDep):
    await db.bookings.delete(id=booking_id)
    await db.commit()
    return {"status": "OK"}
