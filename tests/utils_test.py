from typing import Sequence
from uuid import UUID

from conftest import override_get_db
from sqlalchemy import select

from menu.models import Dish, Menu, Submenu


def fill_menu_table_and_return_id(data) -> UUID:
    session = next(override_get_db())
    menu = Menu(**data)
    session.add(menu)
    session.commit()
    menu_id = menu.id

    return menu_id


def fill_submenu_table_and_return_id(data) -> UUID:
    session = next(override_get_db())
    submenu = Submenu(**data)
    session.add(submenu)
    session.commit()
    submenu_id = submenu.id

    return submenu_id


def fill_dish_table_and_return_id(data) -> UUID:
    session = next(override_get_db())
    dish = Dish(**data)
    session.add(dish)
    session.commit()
    dish_id = dish.id

    return dish_id


def get_menus() -> Sequence[Menu]:
    session = next(override_get_db())
    menus = session.execute(select(Menu)).scalars().all()

    return menus


def get_submenus() -> Sequence[Submenu]:
    session = next(override_get_db())
    submenus = session.execute(select(Submenu)).scalars().all()

    return submenus


def get_dishes() -> Sequence[Dish]:
    session = next(override_get_db())
    dishes = session.execute(select(Dish)).scalars().all()

    return dishes
