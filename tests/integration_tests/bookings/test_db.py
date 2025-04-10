from datetime import datetime

from src.schemas.bookings import SBookingAdd


async def test_booking_crud(db):
    users = await db.users.get_all()
    rooms = await db.rooms.get_all()

    data_booking = SBookingAdd(
        room_id=users[0].id,
        user_id=rooms[0].id,
        date_from=datetime(year=2021, month=1, day=1),
        date_to=datetime(year=2021, month=2, day=1),
        price=100
    )
    new_booking = await db.bookings.add(data_booking)

    #получить бронь и проверить
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.user_id == new_booking.user_id

    #модель для редактирования брони
    data_booking_edit = SBookingAdd(
        room_id=users[0].id,
        user_id=rooms[0].id,
        date_from=datetime(year=2021, month=1, day=1),
        date_to=datetime(year=2021, month=2, day=1),
        price=1000
    )
    await db.bookings.edit(data_booking_edit, id=new_booking.id)
    booking_edit = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking_edit
    assert booking_edit.id == new_booking.id
    assert booking_edit.price == data_booking_edit.price

    #удалить бронь и проверить
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking