from datetime import date

from pydantic import BaseModel
from sqlalchemy import select, func, update

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import SRooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = SRooms

    async def get_filtered_by_time(
            self,
            date_to: date,
            date_from: date,
            hotel_id: int | None = None,
            limit: int = None,
            offset: int = None,
    ) -> list[SRooms]:

        rooms_ids_to_get = rooms_ids_for_booking(date_to, date_from, hotel_id, limit, offset)

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
