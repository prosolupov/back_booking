from httpx import AsyncClient


async def test_add_booking(ac: AsyncClient, authenticated_ac, db):
    room_id = (await db.rooms.get_all())[0].id
    response = await ac.post(
        "bookings",
        json={
            "room_id": room_id,
            "date_to": "2024-12-12",
            "date_from": "2024-12-31",
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert isinstance(response.json()["data"], dict)






