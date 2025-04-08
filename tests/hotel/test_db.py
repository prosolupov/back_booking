from src.schemas.hotels import SHotelsAdd


async def test_add_hotel(db):
    hotel = SHotelsAdd(title="Hotel 5 stars", location="Nairobi")
    await db.hotels.add(hotel)
    await db.commit()