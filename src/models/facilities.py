from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    rooms: Mapped[list["RoomsOrm"]] = relationship(
         back_populates="facilities",
         secondary="rooms_facilities",
     )


class RoomFacilitiesOrm(Base):
    __tablename__ = 'rooms_facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
