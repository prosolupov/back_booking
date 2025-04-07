import json

import pytest
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.schemas.hotels import SHotelsAdd
from src.schemas.rooms import SRoomsAdd

from src.utils.db_manager import DBManager

from src.main import app

@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
         await conn.run_sync(Base.metadata.drop_all)
         await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "first_name": "Kosty",
                "last_name": "Prosolupov",
                "email": "kat@pes.ru",
                "password": "1234"}
            )


@pytest.fixture(scope="session", autouse=True)
async def setup_hotels_and_rooms(setup_database):

    with open("mock_hotels.json", "r") as file:
        hotels = file.read()

    with open("mock_rooms.json", "r") as file:
        rooms = file.read()

    print(f"hotels: {json.loads(hotels)}")

    async with DBManager(async_session_maker_null_pool) as db:
        await db.hotels.add_batch([SHotelsAdd(**hotel) for hotel in json.loads(hotels)])
        await db.rooms.add_batch([SRoomsAdd(**room) for room in json.loads(rooms)])
        await db.commit()