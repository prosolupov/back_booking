from sqlalchemy import delete

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomFacilitiesOrm
from src.schemas.facilities import SFacilities, SRoomsFacilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = SFacilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesOrm
    schema = SRoomsFacilities
