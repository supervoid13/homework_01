from uuid import UUID

from sqlalchemy import distinct, func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.selectable import Select

from .models import Dish, Menu, Submenu


def count_submenus_and_dishes_in_one_request_menu(*, menu_id: UUID | None = None) -> Select:
    major_query = (select(Menu,
                          func.count(distinct(Submenu.id).label('submenus_count')),
                          func.count(distinct(Dish.id)).label('dishes_count'))
                   .join(Menu.submenus, isouter=True)
                   .join(Submenu.dishes, isouter=True))

    if menu_id:
        major_query = major_query.where(Menu.id == menu_id)

    query = major_query.group_by(Menu.id, Menu.title, Menu.description)

    return query


def get_all_data_query() -> Select:
    query = (select(Menu)
             .options(
        joinedload(Menu.submenus)
        .joinedload(Submenu.dishes)))

    return query
