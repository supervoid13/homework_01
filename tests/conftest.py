from typing import Generator

import pytest
from fastapi.testclient import TestClient
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import DB_NAME_TEST, DB_PASSWORD_TEST, DB_PORT_TEST, DB_USER_TEST
from src.main import app
from src.menu.models import Base

test_data = {
    'menu_data': {'title': 'Menu 1', 'description': 'Menu description 1'},
    'submenu_data': {'title': 'Submenu 1', 'description': 'Submenu description 1'},
    'update_menu_data': {'title': 'Updated submenu', 'description': 'Updated submenu description'},
    'update_submenu_data': {'title': 'Updated submenu', 'description': 'Updated submenu description'},
    'dish_data': {'title': 'Dish 1', 'description': 'Dish description 1', 'price': '10.5'},
    'update_dish_data': {'title': 'Updated dish', 'description': 'Updated dish description', 'price': '15.5'}
}

DATABASE_URL_TEST = (f'postgresql+psycopg2://'
                     f'{DB_USER_TEST}:{DB_PASSWORD_TEST}@db_test:{DB_PORT_TEST}/{DB_NAME_TEST}')

engine_test = create_engine(
    url=DATABASE_URL_TEST,
    isolation_level='AUTOCOMMIT'
)

TestingSessionLocal = sessionmaker(bind=engine_test)

client = TestClient(app)


def override_get_db(*args) -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='session', autouse=True)
def setup_redis():
    app.state.redis = Redis(host='redis_test', port=6379, db=0)
    yield
    app.state.redis.flushall()
    app.state.redis.close()


@pytest.fixture(scope='function', autouse=True)
def setup_db():
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)
