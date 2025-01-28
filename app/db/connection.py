from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

DATABASE_URL = settings.DATABASE_URL


@lru_cache
def get_engine():
    return create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
