import os
from collections.abc import Generator
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATA_DIR = Path(os.environ.get("POLICYNEST_DATA_DIR", "/data"))
DB_FOLDER = str(DATA_DIR)
DB_NAME = "policynest.db"
UPLOADS_DIR = DATA_DIR / "uploads"
UPLOADS_MOUNT_PATH = "/data/uploads"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATA_DIR / DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


def ensure_data_dirs() -> None:
    """Create the database and upload directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def get_db() -> Generator[Session]:
    """Yield a SQLAlchemy session for the duration of a request."""
    with SessionLocal() as db:
        yield db


SessionDep = Annotated[Session, Depends(get_db)]
