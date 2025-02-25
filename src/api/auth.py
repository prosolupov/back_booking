from fastapi import APIRouter, HTTPException, Response, Request

from src.database import async_session_maker
from src.schemas.users import SUsersRequestAdd, SUsersAdd
from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.repositories.users import UsersRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register_user(users: SUsersRequestAdd):
    """
    Ручка для регистрации пользователей
    :param users:
    :return: status code
    """
    hashed_password = AuthService().pwd_context.hash(users.password)
    new_user_data = SUsersAdd(
        first_name=users.first_name,
        last_name=users.last_name,
        email=users.email,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {'message': 'Ok'}


@router.post("/login")
async def login_user(
        data: SUsersRequestAdd,
        response: Response
):
    """
    Ручка для авторизации пользователя и генерации jwt токена
    :param data:
    :param response:
    :return: jwt token
    """
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Email doesn't exist")

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        access_token = AuthService().create_access_token({'id': user.id})
        response.set_cookie('access_token', access_token)

        return {'access_token': access_token}


@router.get("/only_auth")
async def only_auth(request: Request):
    """
    Ручка для получения jwt tokena из cookies
    :param request:
    :return:
    """
    access_token = request.cookies.get('access_token') or None
    return {"result": access_token}
