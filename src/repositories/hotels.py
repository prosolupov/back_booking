from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

from src.repositories.utils import rooms_ids_for_booking
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
        """
        Функция по получению всех отелей
        :param location:
        :param title:
        :param limit:
        :param offset:
        :return: Pydantic схему
        """

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

    async def get_filtered_by_time(
            self,
            location: str,
            title: str,
            limit: int,
            offset: int,
            date_to: date,
            date_from: date,
    ) -> list[SHotels]:

        rooms_ids_to_get = rooms_ids_for_booking(date_to=date_to, date_from=date_from, limit=limit, offset=offset)

        hotels_ids_to_get = select(RoomsOrm.hotel_id)

        if location:
            hotels_ids_to_get = hotels_ids_to_get.filter(func.lower(self.model.location).like(f"%{location.lower()}%"))
        if title:
            hotels_ids_to_get = hotels_ids_to_get.filter(func.lower(self.model.title).like(f"%{title.lower()}%"))

        hotels_ids_to_get = (
            hotels_ids_to_get
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        # print(rooms_ids_to_get.compile(compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))
