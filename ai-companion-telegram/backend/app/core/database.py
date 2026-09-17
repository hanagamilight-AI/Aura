"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from .config import settings

# Create database engine
engine = create_engine(
    settings.get_database_url(),
    echo=settings.is_development(),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables.
    Call this on application startup.
    """
    # Import all models here to ensure they're registered with Base
    from ..memory import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
