from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from redis import Redis

from .menu.router import router as menu_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    app.state.redis = Redis(host='redis', port=6379, db=0)
    yield
    app.state.redis.flushall()
    app.state.redis.close()


app = FastAPI(
    title='Menu API',
    lifespan=lifespan,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='Custom title',
        version='2.5.0',
        summary='This is a very custom OpenAPI schema',
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema['info']['x-logo'] = {
        'url': 'https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png'
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(menu_router)
