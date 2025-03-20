from sqlalchemy import delete, insert, select

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomFacilitiesOrm
from src.repositories.mappers.mappers import FacilitiesDataMapper, RoomsFacilitiesDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesOrm
    mapper = RoomsFacilitiesDataMapper

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        """
        Функция по редактированию удобств комнаты
        :param room_id:
        :param facilities_ids:
        :return:
        """
        current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )

        res = await self.session.execute(current_facilities_ids_query)
        current_facilities_ids = res.scalars().all()

        add_facility = list(set(facilities_ids) - set(current_facilities_ids))
        del_facility = list(set(current_facilities_ids) - set(facilities_ids))

        if del_facility:
            del_facility_stmt = (
                delete(self.model)
                .filter(
                   self.model.room_id == room_id,
                   self.model.facility_id.in_(del_facility)
                )
            )
            await self.session.execute(del_facility_stmt)

        if add_facility:
            add_facility_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in add_facility])
            )

            await self.session.execute(add_facility_stmt)
