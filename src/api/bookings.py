from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import RoomNotFoundException, RoomNotFoundHTTPException, \
    HotelNotFoundException, BookingNotFoundException, BookingNotFoundHTTPException
from src.schemas.bookings import SBookingRequest
from src.services.bookings import BookingService

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
    """
    try:
        booking = await BookingService(db).create_booking(user_id=user_id, data_booking=data_booking)
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except HotelNotFoundException as ex:
        raise HotelNotFoundException from ex

    return {"status": "ok", "data": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    """
    Ручка на получения всех бронирований
    """
    bookings = await BookingService(db).get_all_bookings()
    return await bookings


@router.get("/me")
async def get_me_booking(
    db: DBDep,
    user_id: UserIdDep,
):
    """
    Ручка на получения бронирований пользователя
    """
    try:
        booking = await BookingService(db).get_me_booking(user_id=user_id)
    except BookingNotFoundException as ex:
        raise BookingNotFoundHTTPException from ex

    return booking
