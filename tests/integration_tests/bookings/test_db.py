from datetime import date

from src.schemas.bookings import BookingAdd, Booking


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    await db.bookings.add(booking_data)
    assert booking_data

    booking_update = await db.bookings.get_one_or_none(user_id=booking_data.user_id, room_id=booking_data.room_id)
    update_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=300,
    )
    await db.bookings.edit(update_data, user_id=user_id, room_id=room_id)
    assert update_data.price == 300


    booking_delete = await db.bookings.get_one_or_none(user_id=booking_data.user_id, room_id=booking_data.room_id)
    deleted = await db.bookings.delete(user_id=booking_data.user_id, room_id=booking_data.room_id)
    assert deleted is None







