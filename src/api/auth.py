from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.api.dependencies import UserIdDep
from src.schemas.users import SUsersRequestAdd, SUsersAdd, SUsersRequestAuth
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
    try:
        await db.users.add(new_user_data)
    except IntegrityError:
        raise HTTPException(status_code=500, detail="duplicate key value 'users_email'")

    await db.commit()
    return {'message': 'Ok'}


@router.post("/login")
async def login_user(
        db: DBDep,
        data: SUsersRequestAuth,
        response: Response
):
    """
    Ручка для авторизации пользователя и генерации jwt токена
    :param data:
    :param response:
    :return: jwt token
    """
    try:
        user = await db.users.get_user_with_hashed_password(data.email)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

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
async def get_me(db: DBDep, user_id: UserIdDep):
    """
    Ручка для получения jwt tokena из cookies
    :param user_id:
    :return: user
    """
    user = await db.users.get_one_or_none(id=user_id)
    return user
