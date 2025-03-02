from fastapi import APIRouter, Query, HTTPException

from src.schemas.rooms import SRoomsAdd, SRoomsEditPUTCH
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository

router = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router.get("")
async def get_rooms(
        hotel_id: int | None = None,
        page: int | None = Query(1, ge=1),
        per_page: int | None = Query(None, ge=1, lt=10),
):
    per_page = per_page or 5

    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            limit=per_page,
            offset=per_page * (page - 1)
        )


@router.get("/{room_id}")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("")
async def create_room(rooms_data: SRoomsAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).add(rooms_data)
        await session.commit()
        return {"status": "ok"}


@router.put("/{room_id}")
async def edit_all_param_room(room_id: int, rooms_data: SRoomsAdd):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if room:
            await RoomsRepository(session).edit(rooms_data, id=room_id)
            await session.commit()
            return {"status": "ok"}

        raise HTTPException(status_code=404, detail="Room not found")


@router.patch("/{room_id}")
async def edit_one_param_room(room_id: int, rooms_data: SRoomsEditPUTCH):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if room:
            await RoomsRepository(session).edit(rooms_data, exclude_unset=True, id=room_id)
            await session.commit()
            return {"status": "ok"}

        raise HTTPException(status_code=404, detail="Room not found")


@router.delete("")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if room:
            await RoomsRepository(session).delete(id=room_id)
            await session.commit()
            return {"status": "ok"}

        raise HTTPException(status_code=404, detail="Room not found")
