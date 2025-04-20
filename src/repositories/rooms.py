from datetime import date

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import ObjectNotFoundException
from src.models.facilities import RoomFacilitiesOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import SRoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            date_to: date,
            date_from: date,
            hotel_id: int | None = None,
            limit: int = None,
            offset: int = None,
    ) -> list[SRoomWithRels]:
        rooms_ids_to_get = rooms_ids_for_booking(date_to, date_from, hotel_id, limit, offset)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        # print(result.scalars().all()[0].facilities[0].title)

        return [RoomWithRelsDataMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]

    async def get_one_or_none_with_rels(self, *args, **filter_by):
        """
        Функция по получению одной записи переданной модели
        :param args:
        :param kwargs:
        :return: one record model
        """
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            model = result.scalars().one_or_none()
        except NoResultFound:
            raise ObjectNotFoundException

        return RoomWithRelsDataMapper.map_to_domain_entity(model)
