from datetime import date

from src.exceptions import ObjectNotFoundException, HotelNotFoundException, RoomNotFoundException
from src.schemas.facilities import SRoomsFacilitiesAdd
from src.schemas.rooms import SRoomsAddRequest, SRoomsAdd, SRoomsEditPUTCHRequest, SRoomsEditPUTCH, SRooms
from src.services.base import BaseService


class RoomsService(BaseService):

    async def create_room(self, hotel_id: int, rooms_data: SRoomsAddRequest) -> None:
        _room = SRoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())

        try:
            room = await self.db.rooms.add(_room)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex

        list_rooms_facility = [
            SRoomsFacilitiesAdd(
                room_id=room.id,
                facility_id=item
            ) for item in rooms_data.facility_ids
        ]

        await self.db.rooms_facilities.add_batch(list_rooms_facility)
        await self.db.commit()

    async def get_rooms(
        self,
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ):
        per_page = per_page or 5

        rooms = await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_to=date_to,
            date_from=date_from,
            limit=per_page,
            offset=per_page * (page - 1)
        )

        return rooms

    async def get_one_or_none_with_rels(self, hotel_id: int, room_id: int):
        await self.get_room_with_check(room_id=room_id)
        rooms = await self.db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
        return rooms

    async def edit_all_param_room(
        self,
        hotel_id: int,
        room_id: int,
        rooms_data: SRoomsAddRequest
    ):
        _room = SRoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
        await self.get_room_with_check(room_id=room_id)
        await self.db.rooms.edit(_room, id=room_id)

        await self.db.rooms_facilities.set_room_facilities(room_id, rooms_data.facility_ids)
        await self.db.commit()

    async def edit_room_partially(
        self,
        hotel_id: int,
        room_id: int,
        room_data: SRoomsEditPUTCHRequest
    ):
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room = SRoomsEditPUTCH(hotel_id=hotel_id, **_room_data_dict)
        await self.get_room_with_check(room_id=room_id)
        await self.db.rooms.edit(_room, exclude_unset=True, id=room_id, hotel_id=hotel_id)

        if "facility_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facility_ids"])

        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await self.get_room_with_check(room_id=room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()


    async def get_room_with_check(self, room_id: int) -> SRooms:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException