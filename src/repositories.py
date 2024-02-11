from abc import ABC, abstractmethod
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import Row, RowMapping, delete, select, update

from src.database import async_session
from src.menu.models import Base


class AbstractRepository(ABC):
    session_maker = None

    @abstractmethod
    async def retrieve_list(self):
        raise NotImplementedError

    @abstractmethod
    async def retrieve_one(self, pk: UUID):
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update(self, pk: UUID, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, pk: UUID):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    session_maker = async_session

    def __init__(self, model):
        self.model = model

    async def retrieve_list(self) -> Sequence[Row[Base] | RowMapping | Any]:
        async with self.session_maker() as session:
            query = select(self.model)
            result = await session.execute(query)

            return result.scalars().all()

    async def retrieve_one(self, pk: UUID) -> Base:
        async with self.session_maker() as session:
            obj = await session.get(self.model, pk)

            return obj

    async def create(self, data: dict) -> UUID:
        async with self.session_maker() as session:
            obj = self.model(**data)
            session.add(obj)
            await session.commit()

            return obj.id

    async def update(self, pk: UUID, data: dict) -> None:
        async with self.session_maker() as session:
            stmt = (update(self.model)
                    .where(self.model.id == pk)
                    .values(**data)
                    )

            await session.execute(stmt)
            await session.commit()

    async def delete(self, pk: UUID) -> None:
        async with self.session_maker() as session:
            stmt = delete(self.model).where(self.model.id == pk)
            await session.execute(stmt)
            await session.commit()
