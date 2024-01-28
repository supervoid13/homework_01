from conftest import TestingSessionLocal
from menu.models import Menu, Submenu, Dish


def fill_menu_table_and_return_id(data):
    session = TestingSessionLocal()
    menu = Menu(**data)
    session.add(menu)
    session.commit()
    menu_id = menu.id
    session.close()

    return menu_id


def fill_submenu_table_and_return_id(data):
    session = TestingSessionLocal()
    submenu = Submenu(**data)
    session.add(submenu)
    session.commit()
    submenu_id = submenu.id
    session.close()

    return submenu_id


def fill_dish_table_and_return_id(data):
    session = TestingSessionLocal()
    dish = Dish(**data)
    session.add(dish)
    session.commit()
    dish_id = dish.id
    session.close()

    return dish_id
