from pydantic import BaseModel


class HotelsSchema(BaseModel):
    title: str
    location: str


class HotelsSchemaPUTCH(BaseModel):
    title: str | None = None
    location: str | None = None
