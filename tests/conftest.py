from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DB_NAME_TEST, DB_PASSWORD_TEST, DB_PORT_TEST, DB_USER_TEST
from src.main import app
from src.menu.models import Base

DATABASE_URL_TEST = (f'postgresql+asyncpg://'
                     f'{DB_USER_TEST}:{DB_PASSWORD_TEST}@db_test:{DB_PORT_TEST}/{DB_NAME_TEST}')

engine_test = create_async_engine(
    url=DATABASE_URL_TEST,
    isolation_level='AUTOCOMMIT'
)

async_session_test = async_sessionmaker(bind=engine_test, expire_on_commit=False)


async def override_get_db(*args) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        yield session


@pytest.fixture(scope='session', autouse=True)
async def setup_redis() -> AsyncGenerator:
    app.state.redis = Redis(host='redis_test', port=6379, db=0)
    yield
    app.state.redis.flushall()
    app.state.redis.close()


@pytest.fixture(scope='function', autouse=True)
async def setup_db() -> AsyncGenerator:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture()
def test_data() -> dict[str, dict]:
    test_data = {
        'menu_data': {'title': 'Menu 1', 'description': 'Menu description 1'},
        'submenu_data': {'title': 'Submenu 1', 'description': 'Submenu description 1'},
        'update_menu_data': {'title': 'Updated submenu', 'description': 'Updated submenu description'},
        'update_submenu_data': {'title': 'Updated submenu', 'description': 'Updated submenu description'},
        'dish_data': {'title': 'Dish 1', 'description': 'Dish description 1', 'price': '10.5'},
        'update_dish_data': {'title': 'Updated dish', 'description': 'Updated dish description', 'price': '15.5'}
    }

    return test_data
