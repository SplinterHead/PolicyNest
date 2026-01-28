import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_FOLDER = "/data"
DB_NAME = "policynest.db"

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FOLDER}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
