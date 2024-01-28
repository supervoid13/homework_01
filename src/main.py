from fastapi import FastAPI
from src.menu.router import router as menu_router

app = FastAPI(
    title="Menu API"
)

app.include_router(menu_router)
