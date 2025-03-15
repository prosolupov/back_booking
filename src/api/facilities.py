from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import SFacilitiesAdd

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"],
)


@router.get("/")
async def get_all_facilities(db: DBDep):
    facility = await db.facilities.get_all()
    return facility


@router.post("/")
async def create_facility(db: DBDep, data: SFacilitiesAdd):
    facility = await db.facilities.add(data)
    await db.commit()

    return {"status": "ok", "facility": facility}
