import uuid

import utils_test
from conftest import client, test_data
from dependencies_test import (
    override_get_dish_service,
    override_get_menu_service,
    override_get_submenu_service,
)

from src.main import app
from src.menu.dependencies import (
    get_dish_service,
    get_menu_service,
    get_submenu_service,
)

app.dependency_overrides[get_dish_service] = override_get_dish_service
app.dependency_overrides[get_submenu_service] = override_get_submenu_service
app.dependency_overrides[get_menu_service] = override_get_menu_service


def test_get_menus():
    get_menus_url = app.url_path_for('get_menus')

    response = client.get(get_menus_url)
    assert response.status_code == 200
    assert response.json() == []

    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])  # Fill the table with data

    response = client.get(get_menus_url)
    assert response.status_code == 200

    body = response.json()[0]
    assert ((menu_id,
             test_data['menu_data']['title'],
             test_data['menu_data']['description']) == (uuid.UUID(body['id']),
                                                        body['title'],
                                                        body['description']))


def test_get_menu():
    get_menu_url = app.url_path_for('get_menu', menu_id=uuid.uuid4())
    response = client.get(get_menu_url)
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}

    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])

    get_menu_url = app.url_path_for('get_menu', menu_id=menu_id)
    response = client.get(get_menu_url)
    assert response.status_code == 200

    body = response.json()
    assert ((menu_id,
             test_data['menu_data']['title'],
             test_data['menu_data']['description']) == (uuid.UUID(body['id']),
                                                        body['title'],
                                                        body['description']))


def test_add_menu():
    add_menu_url = app.url_path_for('add_menu')
    response = client.post(add_menu_url, json=test_data['menu_data'])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data['menu_data']['title'],
             test_data['menu_data']['description']) == (body['title'],
                                                        body['description']))


def test_update_menus():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    update_menu_url = app.url_path_for('update_menu', menu_id=menu_id)
    response = client.patch(update_menu_url, json=test_data['update_menu_data'])
    assert response.status_code == 200

    body = response.json()
    assert ((menu_id,
             test_data['update_menu_data']['title'],
             test_data['update_menu_data']['description']) == (uuid.UUID(body['id']),
                                                               body['title'],
                                                               body['description']))


def test_delete_menu():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = str(submenu_id)
    utils_test.fill_dish_table_and_return_id(test_data['dish_data'])
    delete_menu_url = app.url_path_for('delete_menu', menu_id=menu_id)

    response = client.delete(delete_menu_url)

    assert response.status_code == 200

    menus = utils_test.get_menus()
    assert menus == []

    submenus = utils_test.get_submenus()
    assert submenus == []

    dishes = utils_test.get_dishes()
    assert dishes == []
