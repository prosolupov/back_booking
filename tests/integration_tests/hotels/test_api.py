async def test_get_hotels(ac):
    response  = await ac.get(
        "/hotels",
        params={
            "date_to": "2024-12-12",
            "date_from": "2024-12-31",
        }
    )

    assert response.status_code == 200