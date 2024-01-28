from conftest import override_get_db
from tests import crud_script
from src.database import get_db
from src.main import app

app.dependency_overrides[get_db] = override_get_db

env = {}


def test_script():
    # Create menu
    menu1 = {"title": "My menu 1", "description": "My menu description 1"}
    response = crud_script.create_menu(menu1)
    assert response.status_code == 201

    body = response.json()
    assert "id" in body

    env["menu_id"] = body["id"]

    # Create submenu
    submenu1 = {"title": "My submenu 1", "description": "My submenu description 1"}
    response = crud_script.create_submenu(env.get("menu_id"), submenu1)
    assert response.status_code == 201

    body = response.json()
    assert "id" in body

    env["submenu_id"] = body["id"]

    # Create dish 1
    dish1 = {"title": "My dish 1", "description": "My dish description 1", "price": "13.50"}
    response = crud_script.create_dish(env.get("menu_id"), env.get("submenu_id"), dish1)
    assert response.status_code == 201

    body = response.json()
    assert "id" in body

    env["dish_id_1"] = body["id"]

    # Create dish 2
    dish2 = {"title": "My dish 2", "description": "My dish description 2", "price": "12.50"}
    response = crud_script.create_dish(env.get("menu_id"), env.get("submenu_id"), dish1)
    assert response.status_code == 201

    body = response.json()
    assert "id" in body

    env["dish_id_2"] = body["id"]

    # Get specific menu
    response = crud_script.get_specific_menu(env.get("menu_id"))
    assert response.status_code == 200

    body = response.json()
    assert body["id"] == env["menu_id"]
    assert body["submenus_count"] == 1
    assert body["dishes_count"] == 2

    # Get specific submenu
    response = crud_script.get_specific_submenu(env.get("menu_id"), env.get("submenu_id"))
    assert response.status_code == 200

    body = response.json()
    assert body["id"] == env["submenu_id"]
    assert body["dishes_count"] == 2

    # Delete submenu
    response = crud_script.delete_submenu(env.get("menu_id"), env.get("submenu_id"))
    assert response.status_code == 200

    del env["submenu_id"]

    # Get list of submenus
    response = crud_script.get_submenus(env.get("menu_id"))
    assert response.status_code == 200

    body = response.json()
    assert body == []

    # Get list of dishes
    response = crud_script.get_dishes(env.get("menu_id"), env.get("submenu_id"))
    assert response.status_code == 200

    body = response.json()
    assert body == []

    # Get specific menu
    response = crud_script.get_specific_menu(env.get("menu_id"))
    assert response.status_code == 200

    body = response.json()
    assert body["id"] == env["menu_id"]
    assert body["submenus_count"] == 0
    assert body["dishes_count"] == 0

    # Delete menu
    response = crud_script.delete_menu(env.get("menu_id"))
    assert response.status_code == 200

    # Get list of menus
    response = crud_script.get_menus()
    assert response.status_code == 200

    body = response.json()
    assert body == []
