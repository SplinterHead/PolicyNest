from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
import shutil
import os
from typing import Optional

from . import models, database

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS config to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/policies/")
def create_policy(
    provider: str = Form(...),
    type: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    premium: float = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    file_location = None
    if file:
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_location = f"{upload_folder}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

    db_policy = models.Policy(
        provider=provider,
        type=type,
        start_date=start_date,
        end_date=end_date,
        premium=premium,
        document_path=file_location
    )
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

@app.get("/policies/")
def read_policies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Policy).offset(skip).limit(limit).all()