from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(
    url=DATABASE_URL,
    pool_size=20,
    # echo=True,
)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db(*args) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
