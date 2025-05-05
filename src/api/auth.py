from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep
from src.exceptions import UserAlreadyExistsException, UserAlreadyExistsHTTPException, \
    IncorrectPasswordException, EmailNotRegisteredException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordHTTPException, UserNotFoundHTTPException, ObjectNotFoundException
from src.schemas.users import SUsersRequestAdd, SUsersRequestAuth
from src.services.auth import AuthService
from src.api.dependencies import DBDep

"""
Auth Service
"""

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register_user(users: SUsersRequestAdd, db: DBDep):
    """
    Ручка для регистрации пользователей
    """

    try:
        user = await AuthService(db).register_user(users)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException

    return {'message': 'ok', 'user': user}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: SUsersRequestAuth,
    response: Response
):
    """
    Ручка для авторизации пользователя и генерации jwt токена
    """
    try:
        access_token = await AuthService(db).login_user(data=data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    except ObjectNotFoundException:
        raise UserNotFoundHTTPException

    response.set_cookie('access_token', access_token)

    return {'access_token': access_token}


@router.post("/logout")
async def logout_user(response: Response):
    '''
    Ручка для выхода
    '''
    response.delete_cookie('access_token')
    return {'status': 'ok'}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    """
    Ручка для получения jwt tokena из cookies
    """
    user = await AuthService(db).get_me(user_id=user_id)

    return user
