from datetime import date

from fastapi import APIRouter, HTTPException, Query

from src.exceptions import ObjectNotFoundException, ObjectDoesExist, RoomNotFoundHTTPException, HotelNotFoundException, \
    RoomNotFoundException
from src.schemas.facilities import SRoomsFacilitiesAdd
from src.schemas.rooms import SRoomsAdd, SRoomsEditPUTCH, SRoomsAddRequest, SRoomsEditPUTCHRequest
from src.api.dependencies import DBDep

from src.services.rooms import RoomsService

router = APIRouter(
    prefix="/hotels",
    tags=["Комнаты"],
)


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, rooms_data: SRoomsAddRequest):
    """
    Ручка для создания номера
    :param db:
    :param hotel_id:
    :param rooms_data:
    :return:
    """
    try:
        room = await RoomsService.create_room(hotel_id=hotel_id, rooms_data=rooms_data)
    except HotelNotFoundException:
        raise RoomNotFoundHTTPException()

    return {"status": "ok", "room": room}


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    date_from: date = Query(example="2025-03-09"),
    date_to: date = Query(example="2025-03-15"),
    hotel_id: int | None = None,
    page: int | None = Query(1, ge=1),
    per_page: int | None = Query(None, ge=1, lt=10),
):
    """
    Ручка для получения всех номер одного отеля
    :param db:
    :param date_to:
    :param date_from:
    :param hotel_id:
    :param page:
    :param per_page:
    :return: Список номеров
    """

    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")

    rooms = await RoomsService(db).get_rooms(
        hotel_id=hotel_id,
        date_to=date_to,
        date_from=date_from,
        page=page,
        per_page=per_page
    )

    return rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    """
    Ручка для получения одного номера
    :param db:
    :param hotel_id:
    :param room_id:
    :return: Room
    """
    try:
        room = RoomsService(db).get_one_or_none_with_rels(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException
    return room


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_all_param_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    rooms_data: SRoomsAddRequest
):
    """
    Ручка для редактирование всех полей номера
    :param db:
    :param hotel_id:
    :param room_id:
    :param rooms_data:
    :return:
    """
    try:
        room = await RoomsService(db).edit_all_param_room(hotel_id=hotel_id, room_id=room_id, rooms_data=rooms_data)
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException

    return {"status": "ok", "room": room}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room_partially(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: SRoomsEditPUTCHRequest
):
    """
    Ручка для редактирование одного или более полей номера
    :param db:
    :param hotel_id:
    :param room_id:
    :param room_data:
    :return:
    """
    try:
        room = await RoomsService(db).edit_room_partially(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException
    return {"status": "ok", "room": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int
):
    """
    Ручка для удаления номера
    :param db:
    :param hotel_id:
    :param room_id:
    :return:
    """
    try:
        await RoomsService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "ok"}
