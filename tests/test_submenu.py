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
async def test_get_submenus(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)

    get_submenus_url = get_url_from_api_route_name(app, 'get_submenus', menu_id=menu_id)

    response = await ac.get(get_submenus_url)
    assert response.status_code == 200
    assert response.json() == []

    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])

    response = await ac.get(get_submenus_url)
    assert response.status_code == 200

    body = response.json()[0]
    assert ((submenu_id,
             test_data['submenu_data']['title'],
             test_data['submenu_data']['description']) == (uuid.UUID(body['id']),
                                                           body['title'],
                                                           body['description']))


@pytest.mark.anyio
async def test_get_submenu(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)

    get_submenu_url = get_url_from_api_route_name(app,
                                                  'get_submenu',
                                                  menu_id=menu_id,
                                                  submenu_id=uuid.uuid4())
    response = await ac.get(get_submenu_url)
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}

    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])

    get_submenu_url = get_url_from_api_route_name(app,
                                                  'get_submenu',
                                                  menu_id=menu_id,
                                                  submenu_id=submenu_id)
    response = await ac.get(get_submenu_url)
    assert response.status_code == 200

    body = response.json()
    assert ((submenu_id,
             test_data['submenu_data']['title'],
             test_data['submenu_data']['description']) == (uuid.UUID(body['id']),
                                                           body['title'],
                                                           body['description']))


@pytest.mark.anyio
async def test_add_submenu(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)

    add_submenu_url = get_url_from_api_route_name(app, 'add_submenu', menu_id=menu_id)

    response = await ac.post(add_submenu_url, json=test_data['submenu_data'])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data['submenu_data']['title'],
             test_data['submenu_data']['description']) == (body['title'],
                                                           body['description']))


@pytest.mark.anyio
async def test_update_submenus(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)

    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])

    update_submenu_url = get_url_from_api_route_name(app,
                                                     'update_submenu',
                                                     menu_id=menu_id,
                                                     submenu_id=submenu_id)

    response = await ac.patch(update_submenu_url, json=test_data['update_submenu_data'])
    assert response.status_code == 200

    body = response.json()
    assert ((submenu_id,
             test_data['update_submenu_data']['title'],
             test_data['update_submenu_data']['description']) == (uuid.UUID(body['id']),
                                                                  body['title'],
                                                                  body['description']))


@pytest.mark.anyio
async def test_delete_submenu(ac: AsyncClient, test_data: dict[str, dict]):
    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['submenu_data']['menu_id'] = str(menu_id)

    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])

    delete_submenu_url = get_url_from_api_route_name(app,
                                                     'delete_submenu',
                                                     menu_id=menu_id,
                                                     submenu_id=submenu_id)
    response = await ac.delete(delete_submenu_url)

    assert response.status_code == 200

    submenus = await utils_test.get_submenus()
    assert submenus == []
