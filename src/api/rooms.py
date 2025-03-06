from fastapi import APIRouter, Query, HTTPException

from src.schemas.rooms import SRoomsAdd, SRoomsAddRequest, SRoomsEditPUTCHRequest, SRoomsEditPUTCH
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.api.dependencies import DBDep

router = APIRouter(
    prefix="/hotel",
    tags=["Комнаты"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int | None = None,
        page: int | None = Query(1, ge=1),
        per_page: int | None = Query(None, ge=1, lt=10),
):
    """
    Ручка для получения всех номер одного отеля
    :param hotel_id:
    :param page:
    :param per_page:
    :return: Список номеров
    """
    per_page = per_page or 5

    return await db.rooms.get_all(
        hotel_id=hotel_id,
        limit=per_page,
        offset=per_page * (page - 1)
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    """
    Ручка для получения одного номера
    :param hotel_id:
    :param room_id:
    :return: Номер
    """
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, rooms_data: SRoomsAddRequest):
    """
    Ручка для создания номера
    :param hotel_id:
    :param rooms_data:
    :return:
    """
    _room = SRoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    await db.rooms.add(_room)
    await db.commit()
    return {"status": "ok"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_all_param_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        rooms_data: SRoomsAddRequest
):
    """
    Ручка для редактирование всех полей номера
    :param hotel_id:
    :param room_id:
    :param rooms_data:
    :return:
    """
    _room = SRoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    room = await db.rooms.get_one_or_none(id=room_id)
    if room:
        await db.rooms.edit(_room, id=room_id)
        await db.commit()
        return {"status": "ok"}

    raise HTTPException(status_code=404, detail="Room not found")


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_one_param_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        rooms_data: SRoomsEditPUTCHRequest):
    """
    Ручка для редактирование одного или более полей номера
    :param hotel_id:
    :param room_id:
    :param rooms_data:
    :return:
    """
    _room = SRoomsEditPUTCH(hotel_id=hotel_id, **rooms_data.model_dump(exclude_unset=True))
    room = await db.rooms.get_one_or_none(id=room_id)
    if room:
        await db.rooms.edit(_room, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        db.commit()
        return {"status": "ok"}

    raise HTTPException(status_code=404, detail="Room not found")


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    """
    Ручка для удаления номера
    :param hotel_id:
    :param room_id:
    :return:
    """
    room = await db.rooms.get_one_or_none(id=room_id)
    if room:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await db.commit()
        return {"status": "ok"}

    raise HTTPException(status_code=404, detail="Room not found")
