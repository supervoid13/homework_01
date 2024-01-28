from fastapi.exceptions import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.sql import func, distinct
from sqlalchemy.orm import Session

from src.menu.models import Menu, Submenu, Dish
from src.menu.schemas import MenuCreateUpdate, SubmenuCreateUpdate, DishCreateUpdate


# ////////////////////////////////////////////////////////////////////////////

# CRUD for Menu


def get_menus(session: Session):
    query = select(Menu)
    result = session.execute(query)
    menus = result.scalars().all()

    return menus


def get_menu_by_pk(session: Session, menu_id: str):
    menu = session.get(Menu, menu_id)

    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


def add_new_menu(session: Session, data: MenuCreateUpdate):
    menu = Menu(**data.model_dump())
    session.add(menu)
    session.commit()

    return menu


def update_menu_by_pk(session: Session, menu_id: str, data: MenuCreateUpdate):
    menu = session.get(Menu, menu_id)

    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    menu.title, menu.description = data.title, data.description

    session.add(menu)
    session.commit()

    return menu


def delete_menu_by_pk(session: Session, menu_id: str):
    menu = session.get(Menu, menu_id)

    session.delete(menu)
    session.commit()


# ////////////////////////////////////////////////////////////////////////////

# CRUD for Submenu


def get_submenus(session: Session, menu_id: str):
    query = select(Submenu).where(Submenu.menu_id == menu_id)
    result = session.execute(query)
    submenus = result.scalars().all()

    return submenus


def get_submenu_by_pk(session: Session, submenu_id: str):
    submenu = session.get(Submenu, submenu_id)

    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


def add_new_submenu(session: Session, menu_id: str, data: SubmenuCreateUpdate):
    submenu = Submenu(**data.model_dump())
    submenu.menu_id = menu_id
    session.add(submenu)
    session.commit()

    return submenu


def update_submenu_by_pk(session: Session, submenu_id: str, data: SubmenuCreateUpdate):
    submenu = session.get(Submenu, submenu_id)

    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    submenu.title, submenu.description = data.title, data.description

    session.add(submenu)
    session.commit()

    return submenu


def delete_submenu_by_pk(session: Session, submenu_id: str):
    submenu = session.get(Submenu, submenu_id)
    session.delete(submenu)
    session.commit()

    return {
        "status": True,
        "message": "The submenu has been deleted"
    }


# ////////////////////////////////////////////////////////////////////////////

# CRUD for Dish


def get_dishes(session: Session, submenu_id: str):
    try:
        query = select(Dish).where(Dish.submenu_id == submenu_id)
        result = session.execute(query)
        dishes = result.scalars().all()

        return dishes
    except (Exception,):
        return []


def get_dish_by_pk(session: Session, dish_id: str):
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return dish


def add_new_dish(session, submenu_id: str, data: DishCreateUpdate):
    dish = Dish(**data.model_dump())
    dish.submenu_id = submenu_id
    session.add(dish)
    session.commit()

    return dish


def update_dish_by_pk(session: Session, dish_id: str, data: DishCreateUpdate):
    dish = session.get(Dish, dish_id)

    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")

    dish.title, dish.description, dish.price = data.title, data.description, data.price

    session.add(dish)
    session.commit()

    return dish


def delete_dish_by_pk(session: Session, dish_id: str):
    stmt = delete(Dish).where(Dish.id == dish_id)
    session.execute(stmt)
    session.commit()

    return {
        "status": True,
        "message": "The dish has been deleted"
    }


def count_submenus_and_dishes_in_one_request(session: Session, menu_id: str):
    response = (session.query(Menu,
                              func.count(distinct(Submenu.id).label("submenus_count")),
                              func.count(distinct(Dish.id)).label("dishes_count"))
                .join(Menu.submenus, isouter=True).join(Submenu.dishes, isouter=True)
                .where(Menu.id == menu_id)
                .group_by(Menu.id, Menu.title, Menu.description)).first()
    if not response:
        raise HTTPException(status_code=404, detail="menu not found")

    return response
