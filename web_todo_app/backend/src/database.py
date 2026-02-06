from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from contextlib import contextmanager


# Get database URL from environment, default to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine based on database type
if DATABASE_URL.startswith("sqlite"):
    # For SQLite, use StaticPool and check_same_thread=False
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        poolclass=StaticPool,
    )
else:
    # For PostgreSQL/other databases
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(bind=engine)


from contextlib import contextmanager
from contextlib import closing


from fastapi import Depends

def get_session():  # This will be used with Depends()
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# Create a dependency that can be used with FastAPI
SessionDep = Depends(get_session)


def get_session_override():
    """Dependency override for testing."""
    yield get_session()