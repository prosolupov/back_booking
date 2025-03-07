from src.repositories.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.schemas.bookings import SBooking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = SBooking
