from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import async_session_maker
from src.schemas.users import SUsersRequestAdd, SUsersAdd
from src.repositories.users import UsersRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(users: SUsersRequestAdd):
    hashed_password = pwd_context.hash(users.password)
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
