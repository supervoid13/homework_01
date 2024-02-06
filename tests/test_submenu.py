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
from src.utils import get_url_from_api_route_name

app.dependency_overrides[get_dish_service] = override_get_dish_service
app.dependency_overrides[get_submenu_service] = override_get_submenu_service
app.dependency_overrides[get_menu_service] = override_get_menu_service


def test_get_submenus():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = menu_id

    get_submenus_url = get_url_from_api_route_name(app, 'get_submenus', menu_id=menu_id)

    response = client.get(get_submenus_url)
    assert response.status_code == 200
    assert response.json() == []

    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])  # Fill the table with data

    response = client.get(get_submenus_url)
    assert response.status_code == 200

    body = response.json()[0]
    assert ((submenu_id,
             test_data['submenu_data']['title'],
             test_data['submenu_data']['description']) == (uuid.UUID(body['id']),
                                                           body['title'],
                                                           body['description']))


def test_get_submenu():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = menu_id

    get_submenu_url = get_url_from_api_route_name(app,
                                                  'get_submenu',
                                                  menu_id=menu_id,
                                                  submenu_id=uuid.uuid4())
    response = client.get(get_submenu_url)
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}

    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])

    get_submenu_url = get_url_from_api_route_name(app,
                                                  'get_submenu',
                                                  menu_id=menu_id,
                                                  submenu_id=submenu_id)
    response = client.get(get_submenu_url)
    assert response.status_code == 200

    body = response.json()
    assert ((submenu_id,
             test_data['submenu_data']['title'],
             test_data['submenu_data']['description']) == (uuid.UUID(body['id']),
                                                           body['title'],
                                                           body['description']))


def test_add_submenu():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)

    add_submenu_url = get_url_from_api_route_name(app, 'add_submenu', menu_id=menu_id)

    response = client.post(add_submenu_url, json=test_data['submenu_data'])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data['submenu_data']['title'],
             test_data['submenu_data']['description']) == (body['title'],
                                                           body['description']))


def test_update_submenus():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)

    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])

    update_submenu_url = get_url_from_api_route_name(app,
                                                     'update_submenu',
                                                     menu_id=menu_id,
                                                     submenu_id=submenu_id)

    response = client.patch(update_submenu_url, json=test_data['update_submenu_data'])
    assert response.status_code == 200

    body = response.json()
    assert ((submenu_id,
             test_data['update_submenu_data']['title'],
             test_data['update_submenu_data']['description']) == (uuid.UUID(body['id']),
                                                                  body['title'],
                                                                  body['description']))


def test_delete_submenu():
    menu_id = utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = menu_id

    submenu_id = utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])

    delete_submenu_url = get_url_from_api_route_name(app,
                                                     'delete_submenu',
                                                     menu_id=menu_id,
                                                     submenu_id=submenu_id)
    response = client.delete(delete_submenu_url)

    assert response.status_code == 200

    submenus = utils_test.get_submenus()
    assert submenus == []
