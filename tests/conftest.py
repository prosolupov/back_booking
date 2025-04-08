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


@pytest.fixture()
async def db():
    async with DBManager(async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "first_name": "Kosty",
            "last_name": "Prosolupov",
            "email": "kat@pes.ru",
            "password": "1234"
        }
    )


@pytest.fixture(scope="session", autouse=True)
async def setup_hotels_and_rooms(setup_database):
    with open("tests/mock_hotels.json") as file:
        hotels = json.load(file)

    with open("tests/mock_rooms.json") as file:
        rooms = json.load(file)

    async with DBManager(async_session_maker_null_pool) as db_:
        await db_.hotels.add_batch([SHotelsAdd.model_validate(hotel) for hotel in hotels])
        await db_.rooms.add_batch([SRoomsAdd.model_validate(room) for room in rooms])
        await db_.commit()
