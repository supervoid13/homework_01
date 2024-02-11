from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.menu.models import Dish, Menu, Submenu
from src.repositories import SQLAlchemyRepository


class MenuRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Menu)

    async def retrieve_list(self) -> list[Menu]:
        async with (self.session_maker() as session):
            query = select(self.model).options(selectinload(self.model.submenus)
                                               .selectinload(Submenu.dishes))
            result = await session.execute(query)

            return result.scalars().all()

    async def retrieve_one(self, pk: UUID) -> Menu:
        async with self.session_maker() as session:
            query = (select(self.model).options(selectinload(self.model.submenus)
                                                .selectinload(Submenu.dishes))
                     .where(self.model.id == pk))
            res = await session.execute(query)

            return res.scalars().first()


class SubmenuRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Submenu)

    async def retrieve_list(self) -> list[Submenu]:
        async with self.session_maker() as session:
            query = select(self.model).options(selectinload(self.model.dishes))
            result = await session.execute(query)

            return result.scalars().all()

    async def retrieve_one(self, pk: UUID) -> Submenu:
        async with self.session_maker() as session:
            query = (select(self.model).options(selectinload(self.model.dishes))
                     .where(self.model.id == pk))
            res = await session.execute(query)

            return res.scalars().first()


class DishRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Dish)
