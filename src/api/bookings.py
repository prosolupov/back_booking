from fastapi import APIRouter, Response, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import SBookingAdd, SBookingRequest

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.post("")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        data_booking: SBookingRequest,
):
    """
    Ручка для добовления бронирований
    :param db:
    :param user_id:
    :param data_booking:
    :return: status
    """

    room = await db.rooms.get_one_or_none(id=data_booking.room_id)
    if room is None:
        raise HTTPException(status_code=400, detail="Room not found")

    _add_booking = SBookingAdd(user_id=user_id, price=room.price, **data_booking.model_dump())
    booking = await db.bookings.add(_add_booking)
    await db.commit()
    return {"status": "ok", "data": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    """
    Ручка на получения всех бронирований
    :param db:
    :return:
    """
    return await db.bookings.get_all()


@router.get("/me")
async def get_me_booking(
        db: DBDep,
        user_id: UserIdDep,
):
    """
    Ручка на получения бронирований пользователя
    :param db:
    :param user_id:
    :return:
    """
    return await db.bookings.get_filtered(user_id=user_id)
