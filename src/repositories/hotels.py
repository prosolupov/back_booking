from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location: str,
            title: str,
            limit: int,
            offset: int
    ):
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
        return result.scalars().all()
