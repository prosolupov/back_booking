from datetime import date
from pydantic import BaseModel


class SBookingAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class SBooking(SBookingAdd):
    id: int


class SBookingRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date
