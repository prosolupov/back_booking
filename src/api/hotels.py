from fastapi import APIRouter, Query
from src.schemas.hotels import Hotel, HotelPUTCH

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get('')
def get_hotels(
        id: int | None = Query(None),
        title: str | None = Query(None),
        page: int | None = Query(None, ge=1),
        per_page: int | None = Query(None, ge=1, lt=10),
):
    list_hotel = []

    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        list_hotel.append(hotel[page:per_page])

    return list_hotel[per_page * (page - 1)][:per_page]


@router.put("/{hotel_id}")
def edit_all_hotel(hotel_id: int, schema_hotel: Hotel):
    global hotels

    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    hotel['title'] = schema_hotel.title
    hotel['name'] = schema_hotel.name
    return {'status': 'ok'}


@router.patch("/{hotel_id}")
def edit_one_param_hotel(hotel_id: int, schema_hotel: HotelPUTCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]

    if schema_hotel.name:
        hotel['name'] = schema_hotel.name
    if schema_hotel.title:
        hotel['title'] = schema_hotel.title

    return {'status': 'ok'}
