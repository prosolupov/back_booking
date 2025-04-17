from fastapi import HTTPException

from src.repositories.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import SBookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def add_booking(self, data: SBookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_to=data.date_to,
            date_from=data.date_from,
            hotel_id=hotel_id
        )

        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        print(f"ROOMS_ID = {rooms_ids_to_book}")
        print(f"ROOMS_ID = {data.room_id}")

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise HTTPException(500)