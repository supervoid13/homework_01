import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from config import DB_PORT_TEST, DB_USER_TEST, DB_PASSWORD_TEST, DB_NAME_TEST
from src.menu.models import Base
from src.main import app

test_data = {
    "menu_data": {"title": "Menu 1", "description": "Menu description 1"},
    "submenu_data": {"title": "Submenu 1", "description": "Submenu description 1"},
    "update_menu_data": {"title": "Updated submenu", "description": "Updated submenu description"},
    "update_submenu_data": {"title": "Updated submenu", "description": "Updated submenu description"},
    "dish_data": {"title": "Dish 1", "description": "Dish description 1", "price": "10.5"},
    "update_dish_data": {"title": "Updated dish", "description": "Updated dish description", "price": "15.5"}
}

DATABASE_URL_TEST = (f"postgresql+psycopg2://"
                     f"{DB_USER_TEST}:{DB_PASSWORD_TEST}@db_test:{DB_PORT_TEST}/{DB_NAME_TEST}")

engine_test = create_engine(
    url=DATABASE_URL_TEST,
)

TestingSessionLocal = sessionmaker(bind=engine_test)

Base.metadata.create_all(engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)
