from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func
from src.schemas.hotels import SHotels


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = SHotels

    async def get_all(
            self,
            location: str,
            title: str,
            limit: int,
            offset: int
    ) -> list[SHotels]:
        query = select(HotelsOrm)

        if location:
            query = query.filter(func.lower(self.model.location).like(f"%{location.lower()}%"))
        if title:
            query = query.filter(func.lower(self.model.title).like(f"%{title.lower()}%"))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
