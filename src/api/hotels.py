from datetime import date

from fastapi import APIRouter, Query, HTTPException

from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import SHotelsAdd, SHotelsPUTCH
from src.api.dependencies import DBDep
from src.services.hotels import HotelsService

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.post("")
async def create_hotel(hotel_data: SHotelsAdd, db: DBDep):
    """
    Ручка на создания нового отеля

    :param db:
    :param hotel_data: HotelOrm (title: str, location: str)
    """
    hotel = await HotelsService(db).create_hotel(hotel_data)
    return {"status": "ok", "data": hotel}


@router.get('')
async def get_hotels(
        db: DBDep,
        date_to: date = Query(example="2025-03-09"),
        date_from: date = Query(example="2025-03-15"),
        location: str | None = Query(None),
        title: str | None = Query(None),
        page: int | None = Query(1, ge=1),
        per_page: int | None = Query(None, ge=1, lt=10),
):
    """
    Ручка по получению всех отелей с фильтрацией и пагинацией.
    Филтирация настроена по location и title
    :param date_to:
    :param db:
    :param date_from:
    :param location:
    :param title:
    :param page:
    :param per_page:
    :return:
    """

    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")

    return await HotelsService(db).get_hotels(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        page=page,
        per_page=per_page
    )


@router.get('/{hotel_id}')
async def get_one(db: DBDep, hotel_id: int):
    """
    Ручка для получения одного отеля по id
    :param hotel_id:
    :return: Hotel
    """
    return await HotelsService(db).get_one_hotel(hotel_id=hotel_id)


@router.put("/{hotel_id}")
async def edit_all_hotel(db: DBDep, hotel_id: int, schema_hotel: SHotelsAdd):
    """
    Ручкка для редактирования отеля
    :param hotel_id:
    :param schema_hotel:
    :return:
    """
    try:
        await HotelsService(db).edit_all_hotel(hotel_id=hotel_id, schema_hotel=schema_hotel)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException


@router.patch("/{hotel_id}")
async def edit_hotel_partially(db: DBDep, schema_hotel: SHotelsPUTCH, hotel_id: int):
    """
    Ручкка для частичного редактирования отеля
    :param schema_hotel:
    :param hotel_id:
    :return:
    """
    try:
        await HotelsService(db).edit_hotel_partially(hotel_id=hotel_id, schema_hotel=schema_hotel)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    """
    Ручка для отеля по id
    :param hotel_id:
    :return:
    """
    try:
        await HotelsService(db).delete_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException
