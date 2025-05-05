from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import SFacilitiesAdd
from src.services.facilities import FacilityService
from src.tasks.tasks import test_task

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"],
)


@router.post("")
async def create_facility(db: DBDep, data: SFacilitiesAdd):
    """
    Ручка для создания удобств
    """
    facility = await FacilityService(db).create_facility(data)
    return {"status": "ok", "facility": facility}


@router.get("")
@cache()
async def get_all_facilities(db: DBDep):
    """
    Получение всех удобств
    """
    return await FacilityService(db).get_all_facilities()
