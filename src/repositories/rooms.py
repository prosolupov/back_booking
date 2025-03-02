from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import SRooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = SRooms

    async def get_all(
            self,
            hotel_id: int | None = None,
            limit: int = None,
            offset: int = None,
    ) -> list[SRooms]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

