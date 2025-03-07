from src.repositories.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.schemas.bookings import SBookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = SBookingAdd
