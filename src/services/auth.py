from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from sqlalchemy.exc import NoResultFound

from src.config import settings
from src.exceptions import ObjectDoesExist, UserAlreadyExistsException, EmailNotRegisteredException, \
    IncorrectPasswordException, ObjectNotFoundException
from src.schemas.users import SUsersRequestAdd, SUsersAdd, SUsersRequestAuth
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

    async def register_user(self, users: SUsersRequestAdd):
        hashed_password = self.pwd_context.hash(users.password)

        new_user_data = SUsersAdd(
            first_name=users.first_name,
            last_name=users.last_name,
            email=users.email,
            hashed_password=hashed_password,
        )
        try:
            user = await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectDoesExist as ex:
            raise UserAlreadyExistsException from ex

        return user

    async def login_user(self, data: SUsersRequestAuth) -> str:
        try:
            user = await self.db.users.get_user_with_hashed_password(email=data.email)
        except NoResultFound as ex:
            raise ObjectNotFoundException from ex

        if not user:
            raise EmailNotRegisteredException

        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException

        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_me(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
