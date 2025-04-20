from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException
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
    try:
        room = await db.rooms.get_one(id=data_booking.room_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=400, detail="Номер не найден")

    try:
        hotel = await db.hotels.get_one(id=room.hotel_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=400, detail="Отель не найден")

    _add_booking = SBookingAdd(user_id=user_id, price=room.price, **data_booking.model_dump())
    booking = await db.bookings.add_booking(_add_booking, hotel_id=hotel.id)
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
