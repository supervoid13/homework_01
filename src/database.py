from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}'

engine = create_engine(
    url=DATABASE_URL,
    pool_size=20
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db(*args) -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
