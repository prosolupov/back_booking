from src.schemas.facilities import SFacilitiesAdd


async def test_add_facilities(db):
    facilities = SFacilitiesAdd(title="WiFi")
    await db.facilities.add(facilities)
    await db.commit()


