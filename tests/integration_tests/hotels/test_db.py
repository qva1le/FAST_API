from src.database import async_session_maker, async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Сочи")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()


