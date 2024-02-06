from abc import ABC, abstractmethod
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import Row, RowMapping, delete, select, update

from src.database import get_db
from src.menu.models import Base


class AbstractRepository(ABC):

    @abstractmethod
    def retrieve_list(self):
        raise NotImplementedError

    @abstractmethod
    def retrieve_one(self, pk: UUID):
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def update(self, pk: UUID, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk: UUID):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    db = get_db

    def __init__(self, model):
        self.model = model

    def retrieve_list(self) -> Sequence[Row[Base] | RowMapping | Any]:
        session = next(self.db())
        query = select(self.model)
        result = session.execute(query)
        objs = result.scalars().all()

        return objs

    def retrieve_one(self, pk: UUID) -> Base:
        session = next(self.db())
        obj = session.get(self.model, pk)

        return obj

    def create(self, data: dict) -> UUID:
        session = next(self.db())
        obj = self.model(**data)
        session.add(obj)
        session.commit()
        pk = obj.id

        return pk

    def update(self, pk: UUID, data: dict) -> None:
        session = next(self.db())
        stmt = (update(self.model)
                .where(self.model.id == pk)
                .values(**data)
                )

        session.execute(stmt)
        session.commit()

    def delete(self, pk: UUID) -> None:
        session = next(self.db())
        stmt = delete(self.model).where(self.model.id == pk)
        session.execute(stmt)
        session.commit()
