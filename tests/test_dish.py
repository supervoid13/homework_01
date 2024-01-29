import uuid
from conftest import client, override_get_db, test_data, TestingSessionLocal

import utils
from src.database import get_db
from src.main import app
from src.menu.crud import get_dishes

app.dependency_overrides[get_db] = override_get_db


def test_get_dishes():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = menu_id
    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])
    test_data["dish_data"]["submenu_id"] = submenu_id

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200
    assert response.json() == []

    dish_id = utils.fill_dish_table_and_return_id(test_data["dish_data"])  # Fill the table with data

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200

    body = response.json()[0]
    assert ((dish_id,
             test_data["dish_data"]["title"],
             test_data["dish_data"]["description"],
             test_data["dish_data"]["price"])
            == (uuid.UUID(body["id"]), body["title"], body["description"], body["price"]))


def test_get_dish():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = menu_id
    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])
    test_data["dish_data"]["submenu_id"] = submenu_id

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}

    dish_id = utils.fill_dish_table_and_return_id(test_data["dish_data"])

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200

    body = response.json()
    assert ((dish_id,
             test_data["dish_data"]["title"],
             test_data["dish_data"]["description"],
             test_data["dish_data"]["price"])
            == (uuid.UUID(body["id"]), body["title"], body["description"], body["price"]))


def test_add_dish():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = str(menu_id)
    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])
    test_data["dish_data"]["submenu_id"] = str(submenu_id)

    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/",
                           json=test_data["dish_data"])
    assert response.status_code == 201

    body = response.json()
    assert ((test_data["dish_data"]["title"],
             test_data["dish_data"]["description"],
             test_data["dish_data"]["price"])
            == (body["title"], body["description"], body["price"]))


def test_update_dish():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = str(menu_id)
    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])
    test_data["dish_data"]["submenu_id"] = submenu_id

    dish_id = utils.fill_dish_table_and_return_id(test_data["dish_data"])
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                            json=test_data["update_dish_data"])
    assert response.status_code == 200

    body = response.json()
    assert ((dish_id,
             test_data["update_dish_data"]["title"],
             test_data["update_dish_data"]["description"],
             test_data["update_dish_data"]["price"])
            == (uuid.UUID(body["id"]), body["title"], body["description"], body["price"]))


def test_delete_dish():
    menu_id = utils.fill_menu_table_and_return_id(test_data["menu_data"])
    test_data["submenu_data"]["menu_id"] = menu_id
    submenu_id = utils.fill_submenu_table_and_return_id(test_data["submenu_data"])
    test_data["dish_data"]["submenu_id"] = submenu_id

    dish_id = utils.fill_dish_table_and_return_id(test_data["dish_data"])
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    assert response.status_code == 200

    with TestingSessionLocal() as session:
        body = get_dishes(session, submenu_id)
        assert body == []
