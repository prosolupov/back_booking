from datetime import date

from fastapi import APIRouter, Query, HTTPException

from src.schemas.hotels import SHotelsAdd, SHotelsPUTCH
from src.api.dependencies import DBDep

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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
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

    per_page = per_page or 5
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (page - 1)
    # )

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (page - 1),
    )


@router.get('/{hotel_id}')
async def get_one(db: DBDep, hotel_id: int):
    """
    Ручка для получения одного отеля по id
    :param hotel_id:
    :return: Hotel
    """
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.put("/{hotel_id}")
async def edit_all_hotel(db: DBDep, hotel_id: int, schema_hotel: SHotelsAdd):
    """
    Ручкка для редактирования отеля
    :param hotel_id:
    :param schema_hotel:
    :return:
    """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)

    if hotel:
        await db.hotels.edit(schema_hotel, id=hotel_id)
        await db.commit()
        return {"status": "ok"}

    raise HTTPException(status_code=404, detail="Item not found")


@router.patch("/{hotel_id}")
async def edit_one_param_hotel(db: DBDep, schema_hotel: SHotelsPUTCH, hotel_id: int):
    """
    Ручкка для частичного редактирования отеля
    :param schema_hotel:
    :param hotel_id:
    :return:
    """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel:
        await db.hotels.edit(schema_hotel, exclude_unset=True, id=hotel_id)
        await db.commit()
        return {"status": "ok"}

    raise HTTPException(status_code=404, detail='Item not found')


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    """
    Ручка для отеля по id
    :param hotel_id:
    :return:
    """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel:
        await db.hotels.delete(id=hotel_id)
        await db.commit()
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail='Item not found')
