from fastapi import APIRouter, Query

from src.database import async_session_maker
from src.schemas.hotels import HotelsSchema, HotelsSchemaPUTCH
from sqlalchemy import insert, select, func
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.post("")
async def create_hotel(hotel_data: HotelsSchema):
    """
    Ручка на создания нового отеля

    :param hotel_data: HotelOrm (title: str, location: str)
    """
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(**hotel_data.model_dump())
        # add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        # await session.execute(add_hotel_stmt)
        await session.commit()

        return {"status": "ok", "data": hotel}


@router.get('')
async def get_hotels(
        location: str | None = Query(None),
        title: str | None = Query(None),
        page: int | None = Query(1, ge=1),
        per_page: int | None = Query(None, ge=1, lt=10),
):
    """
    Ручка по получению всех отелей с фильтрацией и пагинацией.
    Филтирация настроена по location и title
    :param location:
    :param title:
    :param page:
    :param per_page:
    :return:
    """

    per_page = per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (page - 1)
        )


@router.put("/{hotel_id}")
def edit_all_hotel(hotel_id: int, schema_hotel: HotelsSchema):
    global hotels

    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    hotel['title'] = schema_hotel.title
    hotel['name'] = schema_hotel.name
    return {'status': 'ok'}


@router.patch("/{hotel_id}")
def edit_one_param_hotel(hotel_id: int, schema_hotel: HotelsSchemaPUTCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]

    if schema_hotel.name:
        hotel['name'] = schema_hotel.name
    if schema_hotel.title:
        hotel['title'] = schema_hotel.title

    return {'status': 'ok'}
