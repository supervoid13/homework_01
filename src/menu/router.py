from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from menu.schemas import (MenuCreateUpdate, MenuRetrieve, SubmenuRetrieve,
                          SubmenuCreateUpdate, DishRetrieve, DishCreateUpdate)
from menu.utils import get_dishes_count_from_menu
from database import get_db
from menu import crud


router = APIRouter(
    prefix="/api/v1/menus"
)


# ////////////////////////////////////////////////////////////////////////////

# Endpoints for Menu


@router.get("/", response_model=List[MenuRetrieve])
def retrieve_menus(session: Session = Depends(get_db)):
    menus = crud.get_menus(session)

    menus_retrieve = []
    for menu in menus:
        menus_retrieve.append(dict(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=len(menu.submenus),
            dishes_count=get_dishes_count_from_menu(menu)))

    return menus_retrieve


@router.get("/{menu_id}", response_model=MenuRetrieve)
def retrieve_menu(menu_id: str, session: Session = Depends(get_db)):
    menu = crud.get_menu_by_pk(session, menu_id)

    menu_retrieve = dict(
        id=menu.id,
        title=menu.title,
        description=menu.description,
        submenus_count=len(menu.submenus),
        dishes_count=get_dishes_count_from_menu(menu))

    return menu_retrieve


@router.post("/", status_code=201, response_model=MenuRetrieve)
def add_menu(data: MenuCreateUpdate, session: Session = Depends(get_db)):
    menu = crud.add_new_menu(session, data)

    menu_retrieve = dict(id=menu.id,
                         title=menu.title,
                         description=menu.description,
                         submenus_count=len(menu.submenus),
                         dishes_count=get_dishes_count_from_menu(menu))

    return menu_retrieve


@router.patch("/{menu_id}", response_model=MenuRetrieve)
def update_menu(menu_id: str, data: MenuCreateUpdate, session: Session = Depends(get_db)):
    menu = crud.update_menu_by_pk(session, menu_id, data)
    menu.title, menu.description = data.title, data.description

    session.add(menu)
    session.commit()

    menu_retrieve = dict(id=menu.id,
                         title=menu.title,
                         description=menu.description,
                         submenus_count=len(menu.submenus),
                         dishes_count=get_dishes_count_from_menu(menu))

    return menu_retrieve


@router.delete("/{menu_id}")
def delete_menu(menu_id: str, session: Session = Depends(get_db)):
    return crud.delete_menu_by_pk(session, menu_id)


# ////////////////////////////////////////////////////////////////////////////

# Endpoints for Submenu


@router.get("/{menu_id}/submenus", response_model=List[SubmenuRetrieve])
def get_submenus(menu_id: str, session: Session = Depends(get_db)):
    submenus = crud.get_submenus(session, menu_id)

    submenus_retrieve = []
    for submenu in submenus:
        submenus_retrieve.append(dict(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            dishes_count=len(submenu.dishes)))

    return submenus_retrieve


@router.get("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuRetrieve)
def get_submenu(menu_id: str, submenu_id: str, session: Session = Depends(get_db)):
    submenu = crud.get_submenu_by_pk(session, submenu_id)

    submenu_retrieve = dict(
        id=submenu.id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=len(submenu.dishes))

    return submenu_retrieve


@router.post("/{menu_id}/submenus", status_code=201, response_model=SubmenuRetrieve)
def add_submenu(menu_id: str, data: SubmenuCreateUpdate, session: Session = Depends(get_db)):
    submenu = crud.add_new_submenu(session, menu_id, data)

    submenu_retrieve = dict(id=submenu.id,
                            title=submenu.title,
                            description=submenu.description,
                            dishes_count=len(submenu.dishes))

    return submenu_retrieve


@router.patch("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuRetrieve)
def update_submenu(menu_id: str, submenu_id: str, data: SubmenuCreateUpdate,
                   session: Session = Depends(get_db)):
    submenu = crud.update_submenu_by_pk(session, submenu_id, data)
    submenu.title, submenu.description = data.title, data.description

    session.add(submenu)
    session.commit()

    submenu_retrieve = dict(id=submenu.id,
                            title=submenu.title,
                            description=submenu.description,
                            dishes_count=len(submenu.dishes))

    return submenu_retrieve


@router.delete("/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str, session: Session = Depends(get_db)):
    return crud.delete_submenu_by_pk(session, submenu_id)


# ////////////////////////////////////////////////////////////////////////////

# Endpoints for Dish


@router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[DishRetrieve])
def get_dishes(menu_id: str, submenu_id: str, session: Session = Depends(get_db)):
    return crud.get_dishes(session, submenu_id)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishRetrieve)
def get_dish(menu_id: str, submenu_id: str, dish_id: str, session: Session = Depends(get_db)):
    return crud.get_dish_by_pk(session, dish_id)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=201, response_model=DishRetrieve)
def add_dish(menu_id: str, submenu_id: str, data: DishCreateUpdate,
             session: Session = Depends(get_db)):
    return crud.add_new_dish(session, submenu_id, data)


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishRetrieve)
def update_dish(menu_id: str, submenu_id: str, dish_id: str, data: DishCreateUpdate,
                session: Session = Depends(get_db)):
    return crud.update_dish_by_pk(session, dish_id, data)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, session: Session = Depends(get_db)):
    return crud.delete_dish_by_pk(session, dish_id)
