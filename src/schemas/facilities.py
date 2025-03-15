from pydantic import BaseModel


class SFacilitiesAdd(BaseModel):
    title: str


class SFacilities(SFacilitiesAdd):
    id: int
