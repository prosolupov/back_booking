from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.schemas.users import SUsersRequestAdd, SUsersAdd
from src.services.auth import AuthService
from src.repositories.users import UsersRepository

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
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


@router.post("/logout")
async def logout_user(response: Response):
    '''
    Ручка для выхода
    :param response:
    :return: status code
    '''
    response.delete_cookie('access_token')
    return {'status': 'ok'}


@router.get("/me")
async def get_me(user_id: UserIdDep):
    """
    Ручка для получения jwt tokena из cookies
    :param user_id:
    :return: user
    """
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
