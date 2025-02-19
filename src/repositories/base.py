from sqlalchemy import select, insert, literal_column


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalar().one_or_none()

    async def add(self, **kwargs):
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.fetchone()[0]
