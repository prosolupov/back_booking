from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import SFacilitiesAdd
from src.tasks.tasks import test_task

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"],
)


@router.get("/")
#@cache()
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("/")
async def create_facility(db: DBDep, data: SFacilitiesAdd):
    facility = await db.facilities.add(data)
    await db.commit()

    test_task.delay()

    return {"status": "ok", "facility": facility}
