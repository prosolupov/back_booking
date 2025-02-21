from pydantic import BaseModel


class SHotelsAdd(BaseModel):
    title: str
    location: str


class SHotels(SHotelsAdd):
    id: int


class SHotelsPUTCH(BaseModel):
    title: str | None = None
    location: str | None = None
