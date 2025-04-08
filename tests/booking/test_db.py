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
    await db.bookings.add(data_booking)

    #получить бронь и проверить
    print("step 1")
    booking = await db.bookings.get_all()
    assert booking is not None

    print("step 2")
    #модель для редактирования брони
    data_booking_edit = SBookingAdd(
        room_id=users[0].id,
        user_id=rooms[0].id,
        date_from=datetime(year=2021, month=1, day=1),
        date_to=datetime(year=2021, month=2, day=1),
        price=1000
    )
    await db.bookings.edit(data_booking_edit)
    booking_edit = await db.bookings.get_all()
    assert booking_edit[0].price == data_booking_edit.price

    print("step 3")
    #удалить бронь и проверить
    await db.bookings.delete(id=booking[0].id)
    booking = await db.bookings.get_all(booking)
    assert booking == []

    #коммит
    await db.commit()