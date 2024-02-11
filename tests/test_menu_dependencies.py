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
async def test_get_menus_with_dependencies(ac: AsyncClient, test_data: dict[str, dict]):
    url = get_url_from_api_route_name(app, 'get_menus_with_dependencies')
    response = await ac.get(url)
    assert response.status_code == 200
    assert response.json() == []

    menu_id = await utils_test.fill_menu_table_and_return_id(test_data['menu_data'])
    test_data['menu_data']['id'] = str(menu_id)
    test_data['submenu_data']['menu_id'] = str(menu_id)

    submenu_id = await utils_test.fill_submenu_table_and_return_id(test_data['submenu_data'])
    test_data['submenu_data']['id'] = str(submenu_id)

    test_data['dish_data']['submenu_id'] = str(submenu_id)

    dish_id = await utils_test.fill_dish_table_and_return_id(test_data['dish_data'])
    test_data['dish_data']['id'] = str(dish_id)

    response = await ac.get(url)
    assert response.status_code == 200

    expected = [
        {
            **test_data['menu_data']
        }
    ]
    expected[0]['submenus'] = [
        {
            **test_data['submenu_data']
        }
    ]
    expected[0]['submenus'][0]['dishes'] = [
        {
            **test_data['dish_data']
        }
    ]

    assert expected == response.json()
