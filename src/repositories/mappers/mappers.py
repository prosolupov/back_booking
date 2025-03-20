from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import SBooking
from src.schemas.facilities import SFacilities, SRoomsFacilities
from src.schemas.hotels import SHotels
from src.schemas.rooms import SRooms, SRoomWithRels
from src.schemas.users import SUsers, SUsersWithHashedPassword


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = SHotels


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = SRooms


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = SRoomWithRels


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = SFacilities


class RoomsFacilitiesDataMapper(DataMapper):
    db_model = RoomFacilitiesOrm
    schema = SRoomsFacilities


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = SUsers


class SUsersWithHashedPasswordDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = SUsersWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = SBooking
