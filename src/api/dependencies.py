from typing import Annotated
from fastapi import Depends, Request, HTTPException

from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


def get_token(request: Request) -> str:
    """
    Функкция по извлечению access_token из request
    :param request:
    :return: access_token -> str
    """
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        raise HTTPException(status_code=401, detail='No access token')
    return access_token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    """
    Функция по извлечению User ID
    :param token:
    :return: User ID
    """
    data = AuthService().decode_access_token(token)
    return data.get('user_id')


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
