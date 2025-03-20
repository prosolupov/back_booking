from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import relationship, selectinload
from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    """
    Базовый класс репозитория
    """

    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        """
        Функция по получению записей по фильтру
        :param filter_by: 
        :return: 
        """
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **filter_by):
        """
        Функция по получению всех записей сущности БД
        :param args:
        :param kwargs:
        :return: all records model
        """
        return await self.get_filtered()

    async def get_one_or_none(self, *args, **filter_by):
        """
        Функция по получению одной записи переданной модели
        :param args:
        :param kwargs:
        :return: one record model
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        """
        Функция по добавлению записи в БД
        :param data:
        :return: one record model
        """
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add_batch(self, data: list[BaseModel]):
        """
        Функция по добовлению массива записей
        :param data:
        :return:
        """
        stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        """
        Функция по изменению записи в БД
        :param data: Pydantic Shema
        :param exclude_unset: Флаг put или puch
        :param filter_by:
        """
        stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        """
        Функция по удалению записи из БД
        :param filter_by:
        :return: None
        """
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
