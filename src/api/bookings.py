from fastapi import FastAPI, Body, Query, APIRouter, HTTPException

from src.api.dependecies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room

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
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFound:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel: Hotel | None = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.delete("/{bookings_id}")
async def delete_bookings(booking_id: int, db: DBDep):
    await db.bookings.delete(id=booking_id)
    await db.commit()
    return {"status": "OK"}
