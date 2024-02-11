import uuid

import pytest
import utils_test
from dependencies_test import (
    override_get_dish_service,
    override_get_menu_service,
    override_get_submenu_service,
)
from httpx import AsyncClient

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


@pytest.mark.anyio
async def test_get_dishes(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = str(submenu_id)

    get_dishes_url = get_url_from_api_route_name(app,
                                                 'get_dishes',
                                                 menu_id=menu_id,
                                                 submenu_id=submenu_id)
    response = await ac.get(get_dishes_url)
    assert response.status_code == 200
    assert response.json() == []

    dish_id = await utils_test.fill_dish_table_and_return_id(test_data['dish_data'])  # Fill the table with data

    response = await ac.get(get_dishes_url)
    assert response.status_code == 200

    body = response.json()[0]
    assert ((dish_id,
             test_data['dish_data']['title'],
             test_data['dish_data']['description'],
             test_data['dish_data']['price']) == (uuid.UUID(body['id']),
                                                  body['title'],
                                                  body['description'],
                                                  body['price']))


@pytest.mark.anyio
async def test_get_dish(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = str(submenu_id)

    get_dish_url = get_url_from_api_route_name(app,
                                               'get_dish',
                                               menu_id=menu_id,
                                               submenu_id=submenu_id,
                                               dish_id=uuid.uuid4())
    response = await ac.get(get_dish_url)
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}

    dish_id = await utils_test.fill_dish_table_and_return_id(test_data['dish_data'])

    get_dish_url = get_url_from_api_route_name(app,
                                               'get_dish',
                                               menu_id=menu_id,
                                               submenu_id=submenu_id,
                                               dish_id=dish_id)
    response = await ac.get(get_dish_url)
    assert response.status_code == 200

    body = response.json()
    assert ((dish_id,
             test_data['dish_data']['title'],
             test_data['dish_data']['description'],
             test_data['dish_data']['price']) == (uuid.UUID(body['id']),
                                                  body['title'],
                                                  body['description'],
                                                  body['price']))


@pytest.mark.anyio
async def test_add_dish(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = str(submenu_id)

    add_dish_url = get_url_from_api_route_name(app,
                                               'add_dish',
                                               menu_id=menu_id,
                                               submenu_id=submenu_id)
    response = await ac.post(add_dish_url, json=test_data['dish_data'])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data['dish_data']['title'],
             test_data['dish_data']['description'],
             test_data['dish_data']['price']) == (body['title'],
                                                  body['description'],
                                                  body['price']))


@pytest.mark.anyio
async def test_update_dish(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = str(submenu_id)

    dish_id = await utils_test.fill_dish_table_and_return_id(test_data['dish_data'])

    update_dish_url = get_url_from_api_route_name(app,
                                                  'update_dish',
                                                  menu_id=menu_id,
                                                  submenu_id=submenu_id,
                                                  dish_id=dish_id)
    response = await ac.patch(update_dish_url, json=test_data['update_dish_data'])
    assert response.status_code == 200

    body = response.json()
    assert ((dish_id,
             test_data['update_dish_data']['title'],
             test_data['update_dish_data']['description'],
             test_data['update_dish_data']['price']) == (uuid.UUID(body['id']),
                                                         body['title'], body['description'],
                                                         body['price']))


@pytest.mark.anyio
async def test_delete_dish(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = str(submenu_id)

    dish_id = await utils_test.fill_dish_table_and_return_id(test_data['dish_data'])

    delete_dish_url = get_url_from_api_route_name(app,
                                                  'delete_dish',
                                                  menu_id=menu_id,
                                                  submenu_id=submenu_id,
                                                  dish_id=dish_id)
    response = await ac.delete(delete_dish_url)

    assert response.status_code == 200

    dishes = await utils_test.get_dishes()
    assert dishes == []
