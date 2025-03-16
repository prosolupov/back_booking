from pydantic import BaseModel


class SFacilitiesAdd(BaseModel):
    title: str


class SFacilities(SFacilitiesAdd):
    id: int


class SRoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class SRoomsFacilities(SRoomsFacilitiesAdd):
    id: int
