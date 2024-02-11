from typing import Sequence
from uuid import UUID

from conftest import async_session_test
from sqlalchemy import select

from menu.models import Dish, Menu, Submenu


async def fill_menu_table_and_return_id(data) -> UUID:
    async with async_session_test() as session:
        menu = Menu(**data)
        session.add(menu)
        await session.commit()

        return menu.id


async def fill_submenu_table_and_return_id(data) -> UUID:
    async with async_session_test() as session:
        submenu = Submenu(**data)
        session.add(submenu)
        await session.commit()

        return submenu.id


async def fill_dish_table_and_return_id(data) -> UUID:
    async with async_session_test() as session:
        dish = Dish(**data)
        session.add(dish)
        await session.commit()

        return dish.id


async def get_menus() -> Sequence[Menu]:
    async with async_session_test() as session:
        menus = await session.execute(select(Menu))

        return menus.scalars().all()


async def get_submenus() -> Sequence[Submenu]:
    async with async_session_test() as session:
        submenus = await session.execute(select(Submenu))

        return submenus.scalars().all()


async def get_dishes() -> Sequence[Dish]:
    async with async_session_test() as session:
        dishes = await session.execute(select(Dish))

        return dishes.scalars().all()
