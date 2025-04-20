from httpx import AsyncClient
import pytest

from tests.conftest import get_db_null_pool


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
    async for db_m in get_db_null_pool():
        await db_m.bookings.delete()
        await db_m.commit()



@pytest.mark.parametrize("room_id, date_to, date_from, coll_booking, status_code", [
    (1, "2024-12-31", "2024-12-12", 1, 200),
    (1, "2024-12-31", "2024-12-12", 2, 200),
    (1, "2024-12-31", "2024-12-12", 3, 200),
])
async def test_add_get_bookings(
        room_id,
        date_to,
        date_from,
        coll_booking,
        status_code,
        delete_all_bookings,
        authenticated_ac: AsyncClient,
):
    response_add_booking = await authenticated_ac.post(
        "bookings",
        json={
            "room_id": room_id,
            "date_to": date_to,
            "date_from": date_from,
        }
    )

    response_get_me_booking = await authenticated_ac.get("bookings/me")

    assert response_add_booking.status_code == status_code
    assert response_get_me_booking.status_code == status_code
    assert len(response_get_me_booking.json()) == coll_booking