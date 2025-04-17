from httpx import AsyncClient
import pytest

from src.api.dependencies import get_current_user_id
from src.database import engine_null_pool, Base
from src.services.auth import AuthService


@pytest.mark.parametrize("room_id, date_to, date_from, status_code", [
    (1, "2024-12-31", "2024-12-12", 200),
    (1, "2024-12-31", "2024-12-12", 200),
    (1, "2024-12-31", "2024-12-12", 200),
    (1, "2024-12-31", "2024-12-12", 500),
    (1, "2024-12-31", "2024-12-12", 500),
])
async def test_add_booking(
        room_id: int,
        date_to: str,
        date_from: str,
        status_code: int,
        ac: AsyncClient,
        authenticated_ac, db,

):
    #room_id = (await db.rooms.get_all())[0].id
    response = await ac.post(
        "bookings",
        json={
            "room_id": room_id,
            "date_to": date_to,
            "date_from": date_from,
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        assert response.status_code == status_code
        assert response.json()["status"] == "ok"
        assert isinstance(response.json()["data"], dict)


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async with engine_null_pool.begin() as conn:
        await conn.execute(Base.metadata.tables.get("bookings").delete())
        await conn.commit()



@pytest.mark.parametrize("room_id, date_to, date_from, coll_booking, status_code", [
    (1, "2024-12-31", "2024-12-12", 1, 200),
    (1, "2024-12-31", "2024-12-12", 2, 200),
    (1, "2024-12-31", "2024-12-12", 3, 200),
])
async def test_add_get_bookings(
        delete_all_bookings,
        ac:AsyncClient,
        room_id,
        date_to,
        date_from,
        coll_booking,
        status_code
):
    response_add_booking = await ac.post(
        "bookings",
        json={
            "room_id": room_id,
            "date_to": date_to,
            "date_from": date_from,
        }
    )

    user_id = AuthService().decode_access_token(ac.cookies.get("access_token")).get("id")

    response_get_me_booking = await ac.get(
        "bookings/me",
        params={"user_id": user_id}
    )

    assert response_add_booking.status_code == status_code
    assert response_get_me_booking.status_code == status_code
    assert len(response_get_me_booking.json()) == coll_booking