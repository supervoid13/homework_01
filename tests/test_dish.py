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


def test_get_dishes():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = menu_id
    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = submenu_id

    get_dishes_url = app.url_path_for('get_dishes', menu_id=menu_id, submenu_id=submenu_id)
    response = client.get(get_dishes_url)
    assert response.status_code == 200
    assert response.json() == []

    dish_id = utils_test.fill_dish_table_and_return_id(test_data['dish_data'])  # Fill the table with data

    response = client.get(get_dishes_url)
    assert response.status_code == 200

    body = response.json()[0]
    assert ((dish_id,
             test_data['dish_data']['title'],
             test_data['dish_data']['description'],
             test_data['dish_data']['price']) == (uuid.UUID(body['id']),
                                                  body['title'],
                                                  body['description'],
                                                  body['price']))


def test_get_dish():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = menu_id
    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = submenu_id

    get_dish_url = app.url_path_for('get_dish',
                                    menu_id=menu_id,
                                    submenu_id=submenu_id,
                                    dish_id=uuid.uuid4())
    response = client.get(get_dish_url)
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}

    dish_id = utils_test.fill_dish_table_and_return_id(test_data['dish_data'])

    get_dish_url = app.url_path_for('get_dish',
                                    menu_id=menu_id,
                                    submenu_id=submenu_id,
                                    dish_id=dish_id)
    response = client.get(get_dish_url)
    assert response.status_code == 200

    body = response.json()
    assert ((dish_id,
             test_data['dish_data']['title'],
             test_data['dish_data']['description'],
             test_data['dish_data']['price']) == (uuid.UUID(body['id']),
                                                  body['title'],
                                                  body['description'],
                                                  body['price']))


def test_add_dish():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = str(submenu_id)

    add_dish_url = app.url_path_for('add_dish',
                                    menu_id=menu_id,
                                    submenu_id=submenu_id)
    response = client.post(add_dish_url, json=test_data['dish_data'])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data['dish_data']['title'],
             test_data['dish_data']['description'],
             test_data['dish_data']['price']) == (body['title'],
                                                  body['description'],
                                                  body['price']))


def test_update_dish():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = submenu_id

    dish_id = utils_test.fill_dish_table_and_return_id(test_data['dish_data'])
    update_dish_url = app.url_path_for('update_dish',
                                       menu_id=menu_id,
                                       submenu_id=submenu_id,
                                       dish_id=dish_id)
    response = client.patch(update_dish_url, json=test_data['update_dish_data'])
    assert response.status_code == 200

    body = response.json()
    assert ((dish_id,
             test_data['update_dish_data']['title'],
             test_data['update_dish_data']['description'],
             test_data['update_dish_data']['price']) == (uuid.UUID(body['id']),
                                                         body['title'], body['description'],
                                                         body['price']))


def test_delete_dish():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = menu_id
    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = submenu_id

    dish_id = utils_test.fill_dish_table_and_return_id(test_data['dish_data'])
    delete_dish_url = app.url_path_for('delete_dish',
                                       menu_id=menu_id,
                                       submenu_id=submenu_id,
                                       dish_id=dish_id)
    response = client.delete(delete_dish_url)

    assert response.status_code == 200

    dishes = utils_test.get_dishes()
    assert dishes == []
