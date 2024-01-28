from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    url=DATABASE_URL,
)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
