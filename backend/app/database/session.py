"""
Database engine + session management.

get_db() is injected into every route that needs DB access via
Depends(get_db) — FastAPI handles opening/closing the session per request.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
