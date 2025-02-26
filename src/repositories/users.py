from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import SUsers, SUsersWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = SUsers

    async def get_user_with_hashed_password(self, email: EmailStr) -> SUsersWithHashedPassword:
        """
        Функция для получения пользователя с паролем
        :param email:
        :return: Pydantic схема User с паролем
        """
        query = select(UsersOrm).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()

        return SUsersWithHashedPassword.model_validate(model, from_attributes=True)


