from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis import Redis

from .menu.router import router as menu_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(host='redis', port=6379, db=0)
    yield
    app.state.redis.flushall()
    app.state.redis.close()


app = FastAPI(
    title='Menu API',
    lifespan=lifespan
)

app.include_router(menu_router)
