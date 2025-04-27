from src.schemas.facilities import SFacilitiesAdd
from src.services.base import BaseService


class FacilityService(BaseService):
    async def create_facility(self, data: SFacilitiesAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()
        return facility

    async def get_all_facilities(self):
        return await self.db.facilities.get_all()