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
    room = await db.rooms.get_one_or_none(id=data_booking.room_id)
    if room is None:
        raise HTTPException(status_code=400, detail="Room not found")

    _booking = SBookingAdd(user_id=user_id, price=room.price, **data_booking.model_dump())
    await db.bookings.add(_booking)
    await db.commit()
    return {"user_id": room.price}