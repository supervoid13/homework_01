import uuid
from conftest import client, override_get_db, test_data, TestingSessionLocal

from src.database import get_db
from src.main import app
import utils
from src.menu import crud

app.dependency_overrides[get_db] = override_get_db


def test_get_menus():
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []

    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])  # Fill the table with data

    response = client.get("/api/v1/menus")
    assert response.status_code == 200

    body = response.json()[0]
    assert ((menu_id, test_data["menu_data"]["title"], test_data["menu_data"]["description"])
            == (uuid.UUID(body["id"]), body["title"], body["description"]))


def test_get_menu():
    response = client.get(f"/api/v1/menus/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])

    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

    body = response.json()
    assert ((menu_id, test_data["menu_data"]["title"], test_data["menu_data"]["description"])
            == (uuid.UUID(body["id"]), body["title"], body["description"]))


def test_add_menu():
    response = client.post("/api/v1/menus", json=test_data["menu_data"])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data["menu_data"]["title"], test_data["menu_data"]["description"])
            == (body["title"], body["description"]))


def test_update_menus():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    response = client.patch(f"/api/v1/menus/{menu_id}",
                            json=test_data["update_menu_data"])
    assert response.status_code == 200

    body = response.json()
    assert ((menu_id, test_data["update_menu_data"]["title"], test_data["update_menu_data"]["description"])
            == (uuid.UUID(body["id"]), body["title"], body["description"]))


def test_delete_menu():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = str(menu_id)
    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])
    test_data["dish_data"]["submenu_id"] = str(submenu_id)
    utils.fill_dish_table_and_return_id(test_data["dish_data"])

    response = client.delete(f"/api/v1/menus/{menu_id}")

    assert response.status_code == 200

    with TestingSessionLocal() as session:
        body = crud.get_menus(session)
        assert body == []

    with TestingSessionLocal() as session:
        body = crud.get_submenus(session, menu_id)
        assert body == []

    with TestingSessionLocal() as session:
        body = crud.get_dishes(session, submenu_id)
        assert body == []
