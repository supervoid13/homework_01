from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from redis import Redis

from .menu.models import init_db
from .menu.router import router as menu_router

redis = Redis(host='redis', port=6379, db=0)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    app.state.redis = redis
    await init_db()
    yield
    redis.flushall()
    redis.close()


app = FastAPI(
    title='Menu API',
    lifespan=lifespan,
)

app.include_router(menu_router)
