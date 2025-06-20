import json
from pathlib import Path

from httpx import AsyncClient
from httpx import ASGITransport

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.api.dependecies import DBDep
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker, async_session_maker_null_pool
from src.models import *
from src.main import app
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm

BASE_DIR = Path(__file__).resolve().parent
@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def data_hotels_post():
    hotels_path = BASE_DIR / "mock_hotels.json"
    with open(hotels_path, "r", encoding="utf-8") as file:
        hotels_data = json.load(file)
    async with async_session_maker_null_pool() as session:
        hotel_obj = [HotelsOrm(**data) for data in hotels_data]
        session.add_all(hotel_obj)
        await session.commit()

@pytest.fixture(scope="session", autouse=True)
async def data_rooms_post():
    rooms_path = BASE_DIR / "mock_rooms.json"
    with open(rooms_path, "r", encoding="utf-8") as file:
        rooms_data = json.load(file)
    async with async_session_maker_null_pool() as session:
        room_obj = [RoomsOrm(**data) for data in rooms_data]
        session.add_all(room_obj)
        await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={"email": "kot@pes.com", "password": "1234"}
        )
