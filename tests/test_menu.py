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
async def test_get_menus(ac: AsyncClient, test_data: dict[str, dict]):
    get_menus_url = get_url_from_api_route_name(app, 'get_menus')

    response = await ac.get(get_menus_url)
    assert response.status_code == 200
    assert response.json() == []

    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])  # Fill the table with data

    response = await ac.get(get_menus_url)
    assert response.status_code == 200

    body = response.json()[0]
    assert ((menu_id,
             test_data['menu_data']['title'],
             test_data['menu_data']['description']) == (uuid.UUID(body['id']),
                                                        body['title'],
                                                        body['description']))


@pytest.mark.anyio
async def test_get_menu(ac: AsyncClient, test_data: dict[str, dict]):
    get_menu_url = get_url_from_api_route_name(app, 'get_menu', menu_id=uuid.uuid4())

    response = await ac.get(get_menu_url)
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}

    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])

    get_menu_url = app.url_path_for('get_menu', menu_id=menu_id)
    response = await ac.get(get_menu_url)
    assert response.status_code == 200

    body = response.json()
    assert ((menu_id,
             test_data['menu_data']['title'],
             test_data['menu_data']['description']) == (uuid.UUID(body['id']),
                                                        body['title'],
                                                        body['description']))


@pytest.mark.anyio
async def test_add_menu(ac: AsyncClient, test_data: dict[str, dict]):
    add_menu_url = get_url_from_api_route_name(app, 'add_menu')

    response = await ac.post(add_menu_url, json=test_data['menu_data'])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data['menu_data']['title'],
             test_data['menu_data']['description']) == (body['title'],
                                                        body['description']))


@pytest.mark.anyio
async def test_update_menus(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])

    update_menu_url = get_url_from_api_route_name(app, 'update_menu', menu_id=menu_id)

    response = await ac.patch(update_menu_url, json=test_data['update_menu_data'])
    assert response.status_code == 200

    body = response.json()
    assert ((menu_id,
             test_data['update_menu_data']['title'],
             test_data['update_menu_data']['description']) == (uuid.UUID(body['id']),
                                                               body['title'],
                                                               body['description']))


@pytest.mark.anyio
async def test_delete_menu(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)
    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['dish_data']['submenu_id'] = str(submenu_id)
    await utils_test.fill_dish_table_and_return_id(test_data['dish_data'])

    delete_menu_url = get_url_from_api_route_name(app, 'delete_menu', menu_id=menu_id)

    response = await ac.delete(delete_menu_url)

    assert response.status_code == 200

    menus = await utils_test.get_menus()
    assert menus == []

    submenus = await utils_test.get_submenus()
    assert submenus == []

    dishes = await utils_test.get_dishes()
    assert dishes == []
