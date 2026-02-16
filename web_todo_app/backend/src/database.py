from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool, NullPool
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from contextlib import contextmanager
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Get database URL from environment, default to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Detect if running in serverless environment (Vercel)
IS_SERVERLESS = os.getenv("VERCEL") is not None

# Create engine based on database type
try:
    if DATABASE_URL.startswith("sqlite"):
        # For SQLite, use StaticPool and check_same_thread=False
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},  # Needed for SQLite
            poolclass=StaticPool,
        )
        logger.info("Database engine created for SQLite")
    else:
        # For PostgreSQL - use NullPool in serverless, connection pooling otherwise
        if IS_SERVERLESS:
            # Serverless: no connection pooling, NeonDB pooler handles it
            engine = create_engine(
                DATABASE_URL,
                poolclass=NullPool,
                echo=False
            )
            logger.info("Database engine created for PostgreSQL (serverless mode with NullPool)")
        else:
            # Local development: use connection pooling
            engine = create_engine(
                DATABASE_URL,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False
            )
            logger.info("Database engine created for PostgreSQL with connection pooling")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    try:
        SQLModel.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


from contextlib import contextmanager
from contextlib import closing


from fastapi import Depends

def get_session():  # This will be used with Depends()
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


# Create a dependency that can be used with FastAPI
SessionDep = Depends(get_session)


def get_session_override():
    """Dependency override for testing."""
    yield get_session()