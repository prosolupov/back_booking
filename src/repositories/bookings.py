from fastapi import HTTPException
from sqlalchemy import select, func, insert

from src.models import RoomsOrm
from src.repositories.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.rooms import RoomsRepository
from src.schemas.bookings import SBookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def add_booking(self, data: SBookingAdd):
        rooms_count_query = (
            select(func.count(data.room_id))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= data.date_to,
                BookingsOrm.date_to >= data.date_from
            )
        )

        rooms_quantity_query = select(RoomsOrm.quantity).select_from(RoomsOrm).where(RoomsOrm.id == data.room_id)

        rooms_count_result = await self.session.execute(rooms_count_query)
        rooms_quantity_result = await self.session.execute(rooms_quantity_query)

        rooms_count = rooms_count_result.scalar()
        rooms_quantity = rooms_quantity_result.scalar()

        if rooms_quantity <= rooms_count:
            raise HTTPException(status_code=404)

        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)