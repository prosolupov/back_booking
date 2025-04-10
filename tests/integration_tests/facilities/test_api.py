from httpx import AsyncClient


async def test_create_facility(ac: AsyncClient):
    response = await ac.post(
        "/facilities",
        json={
            "title": "WiFi"
        }
    )

    assert response.status_code == 200


async def test_get_all_facilities(ac: AsyncClient):
    response = await ac.get("/facilities")

    assert response.status_code == 200
