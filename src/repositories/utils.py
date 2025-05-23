from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_booking(
        date_to: date,
        date_from: date,
        hotel_id: int | None = None,
        limit: int = None,
        offset: int = None,
):
    rooms_count = (
        select(BookingsOrm.room_id, func.count('*').label('count_booked'))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from
        )
        .group_by(BookingsOrm.room_id)
        .cte(name='rooms_count')
    )

    rooms_left_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.count_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, rooms_count.c.room_id == RoomsOrm.id)
        .cte(name="rooms_left_table")
    )

    #query = select(self.model).filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotels = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )

    if hotel_id is not None:
        rooms_ids_for_hotels = (
            rooms_ids_for_hotels
            .filter_by(hotel_id=hotel_id))

    rooms_ids_for_hotels = (
        rooms_ids_for_hotels
        .subquery(name='rooms_ids_for_hotels')
    )

    query = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotels),
        )
    )

    rooms_ids_to_get = (
        query
        .limit(limit)
        .offset(offset)
    )

    return rooms_ids_to_get