import pytest
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

app.dependency_overrides[get_dish_service] = override_get_dish_service
app.dependency_overrides[get_submenu_service] = override_get_submenu_service
app.dependency_overrides[get_menu_service] = override_get_menu_service

env = {}


@pytest.mark.anyio
async def test_script(ac: AsyncClient):
    # Create menu
    menu1 = {'title': 'My menu 1', 'description': 'My menu description 1'}
    response = await ac.post('/api/v1/menus/', json=menu1)
    assert response.status_code == 201

    body = response.json()
    assert 'id' in body

    env['menu_id'] = body['id']

    # Create submenu
    submenu1 = {'title': 'My submenu 1', 'description': 'My submenu description 1'}
    response = await ac.post(f"/api/v1/menus/{env.get('menu_id')}/submenus", json=submenu1)
    assert response.status_code == 201

    body = response.json()
    assert 'id' in body

    env['submenu_id'] = body['id']

    # Create dish 1
    dish1 = {'title': 'My dish 1', 'description': 'My dish description 1', 'price': '13.50'}
    response = await ac.post(f'/api/v1/menus/'
                             f"{env.get('menu_id')}/submenus/{env.get('submenu_id')}/dishes",
                             json=dish1)
    assert response.status_code == 201

    body = response.json()
    assert 'id' in body

    env['dish_id_1'] = body['id']

    # Create dish 2
    dish2 = {'title': 'My dish 2', 'description': 'My dish description 2', 'price': '12.50'}
    response = await ac.post(f'/api/v1/menus/'
                             f"{env.get('menu_id')}/submenus/{env.get('submenu_id')}/dishes",
                             json=dish2)
    assert response.status_code == 201

    body = response.json()
    assert 'id' in body

    env['dish_id_2'] = body['id']

    # Get specific menu
    response = await ac.get(f"/api/v1/menus/{env.get('menu_id')}")
    assert response.status_code == 200

    body = response.json()
    assert body['id'] == env['menu_id']
    assert body['submenus_count'] == 1
    assert body['dishes_count'] == 2

    # Get specific submenu
    response = await ac.get(f"/api/v1/menus/{env.get('menu_id')}/submenus/{env.get('submenu_id')}")
    assert response.status_code == 200

    body = response.json()
    assert body['id'] == env['submenu_id']
    assert body['dishes_count'] == 2

    # Delete submenu
    response = await ac.delete(f"/api/v1/menus/{env.get('menu_id')}/submenus/{env.get('submenu_id')}")
    assert response.status_code == 200

    # Get list of submenus
    response = await ac.get(f"/api/v1/menus/{env.get('menu_id')}/submenus")
    assert response.status_code == 200

    body = response.json()
    assert body == []

    # Get list of dishes
    response = await ac.get(f'/api/v1/menus/'
                            f"{env.get('menu_id')}/submenus/{env.get('submenu_id')}/dishes")
    assert response.status_code == 200

    body = response.json()
    assert body == []

    # Get specific menu
    response = await ac.get(f"/api/v1/menus/{env.get('menu_id')}")
    assert response.status_code == 200

    body = response.json()
    assert body['id'] == env['menu_id']
    assert body['submenus_count'] == 0
    assert body['dishes_count'] == 0

    # Delete menu
    response = await ac.delete(f"/api/v1/menus/{env.get('menu_id')}")
    assert response.status_code == 200

    # Get list of menus
    response = await ac.get('/api/v1/menus/')
    assert response.status_code == 200

    body = response.json()
    assert body == []
