from pydantic import BaseModel


class Hotel(BaseModel):
    title: str
    name: str


class HotelPUTCH(BaseModel):
    title: str | None = None
    name: str | None = None
