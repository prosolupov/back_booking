from src.api.dependencies import UserIdDep
from src.exceptions import RoomNotFoundException, ObjectNotFoundException, HotelNotFoundException, \
    BookingNotFoundException
from src.schemas.bookings import SBookingRequest, SBookingAdd
from src.services.base import BaseService


class BookingService(BaseService):

    async def create_booking(self, user_id: int, data_booking: SBookingRequest,):
        try:
            room = await self.db.rooms.get_one(id=data_booking.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex

        try:
            hotel = await self.db.hotels.get_one(id=room.hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

        _add_booking = SBookingAdd(user_id=user_id, price=room.price, **data_booking.model_dump())
        booking = await self.db.bookings.add_booking(_add_booking, hotel_id=hotel.id)
        await self.db.commit()
        return booking


    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_me_booking(self, user_id: int):
        try:
            booking = await self.db.bookings.get_filtered(user_id=user_id)
            return booking
        except ObjectNotFoundException as ex:
            raise BookingNotFoundException from ex