from conftest import client
from httpx import Response

# Menu utils


def get_menus() -> Response:
    return client.get('/api/v1/menus/')


def get_specific_menu(menu_id) -> Response:
    return client.get(f'/api/v1/menus/{menu_id}')


def create_menu(data) -> Response:
    return client.post('/api/v1/menus/', json=data)


def delete_menu(menu_id) -> Response:
    return client.delete(f'/api/v1/menus/{menu_id}')


# Submenu utils

def get_submenus(menu_id) -> Response:
    return client.get(f'/api/v1/menus/{menu_id}/submenus/')


def get_specific_submenu(menu_id, submenu_id) -> Response:
    return client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')


def create_submenu(menu_id, data) -> Response:
    return client.post(f'/api/v1/menus/{menu_id}/submenus/', json=data)


def delete_submenu(menu_id, submenu_id) -> Response:
    return client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')


# Dish utils

def get_dishes(menu_id, submenu_id) -> Response:
    return client.get(f'/api/v1/menus/'
                      f'{menu_id}/submenus/{submenu_id}/dishes/')


def create_dish(menu_id, submenu_id, data) -> Response:
    return client.post(f'/api/v1/menus/'
                       f'{menu_id}/submenus/{submenu_id}/dishes/',
                       json=data)
