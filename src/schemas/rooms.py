from pydantic import BaseModel

from src.schemas.facilities import SFacilities


class SRoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int


class SRoomsAddRequest(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    facility_ids: list[int] = []


class SRooms(SRoomsAdd):
    id: int


class SRoomWithRels(SRooms):
    facilities: list[SFacilities]


class SRoomsEditPUTCHRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facility_ids: list[int] = []


class SRoomsEditPUTCH(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
