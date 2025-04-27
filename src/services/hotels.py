from datetime import date

from src.exceptions import ObjectNotFoundException
from src.schemas.hotels import SHotelsAdd, SHotelsPUTCH
from src.services.base import BaseService


class HotelsService(BaseService):

    async def create_hotel(self, hotel_data: SHotelsAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def get_hotels(
            self,
            date_to: date,
            date_from: date,
            location: str | None = None,
            title: str | None = None,
            page: int | None = None,
            per_page: int | None = None,
    ):
        per_page = per_page or 5

        hotels = await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (page - 1),
        )

        return hotels

    async def get_one_hotel(self, hotel_id: int):
        return await self.db.hotels.get_hotel(id=hotel_id)

    async def edit_all_hotel(self, hotel_id: int, schema_hotel: SHotelsAdd):
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)

        if hotel:
            await self.db.hotels.edit(schema_hotel, id=hotel_id)
            await self.db.commit()
            return {"status": "ok"}

        raise ObjectNotFoundException

    async def edit_hotel_partially(self, schema_hotel: SHotelsPUTCH, hotel_id: int):
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)
        if hotel:
            await self.db.hotels.edit(schema_hotel, exclude_unset=True, id=hotel_id)
            await self.db.commit()
            return {"status": "ok"}

        raise ObjectNotFoundException

    async def delete_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)
        if hotel:
            await self.db.hotels.delete(id=hotel_id)
            await self.db.commit()
            return {"status": "ok"}
        raise ObjectNotFoundException
