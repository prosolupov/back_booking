from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import SUsers


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = SUsers