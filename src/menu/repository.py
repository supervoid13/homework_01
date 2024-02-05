from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.menu.models import Dish, Menu, Submenu
from src.repositories import SQLAlchemyRepository


class MenuRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Menu)

    def retrieve_list(self) -> list[Menu]:
        session = next(self.db())
        query = select(self.model).options(selectinload(self.model.submenus))
        result = session.execute(query)
        objs = result.scalars().all()

        return objs

    def retrieve_one(self, pk: UUID) -> Menu:
        session = next(self.db())
        query = (select(self.model).options(selectinload(self.model.submenus))
                 .where(self.model.id == pk))
        res = session.execute(query)
        obj = res.scalars().first()

        return obj


class SubmenuRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Submenu)

    def retrieve_list(self) -> list[Submenu]:
        session = next(self.db())
        query = select(self.model).options(selectinload(self.model.dishes))
        result = session.execute(query)
        objs = result.scalars().all()

        return objs

    def retrieve_one(self, pk: UUID) -> Submenu:
        session = next(self.db())
        query = (select(self.model).options(selectinload(self.model.dishes))
                 .where(self.model.id == pk))
        res = session.execute(query)
        obj = res.scalars().first()

        return obj


class DishRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Dish)
