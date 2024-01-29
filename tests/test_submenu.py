import uuid
from conftest import client, override_get_db, test_data, TestingSessionLocal

import utils
from src.database import get_db
from src.main import app
from src.menu.crud import get_submenus

app.dependency_overrides[get_db] = override_get_db


def test_get_submenus():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = menu_id

    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == []

    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])  # Fill the table with data

    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200

    body = response.json()[0]
    assert ((submenu_id, test_data["submenu_data"]["title"], test_data["submenu_data"]["description"])
            == (uuid.UUID(body["id"]), body["title"], body["description"]))


def test_get_submenu():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = menu_id

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}

    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    body = response.json()
    assert ((submenu_id, test_data["submenu_data"]["title"], test_data["submenu_data"]["description"])
            == (uuid.UUID(body["id"]), body["title"], body["description"]))


def test_add_submenu():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = str(menu_id)

    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=test_data["submenu_data"])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data["submenu_data"]["title"], test_data["submenu_data"]["description"])
            == (body["title"], body["description"]))


def test_update_submenus():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = str(menu_id)

    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
                            json=test_data["update_submenu_data"])
    assert response.status_code == 200

    body = response.json()
    assert ((submenu_id, test_data["update_submenu_data"]["title"], test_data["update_submenu_data"]["description"])
            == (uuid.UUID(body["id"]), body["title"], body["description"]))


def test_delete_submenu():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = menu_id

    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200

    with TestingSessionLocal() as session:
        body = get_submenus(session, menu_id)
        assert body == []
