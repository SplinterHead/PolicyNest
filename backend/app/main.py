import os
import shutil
from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ONBOARDING ENDPOINTS ---


@app.get("/system/status")
def get_system_status(db: Session = Depends(get_db)):
    """Checks if a household exists to determine if onboarding is needed."""
    household = db.query(models.Household).first()
    if household:
        return {"initialized": True, "household": household}
    return {"initialized": False, "household": None}


@app.post("/households/")
def create_household(name: str = Form(...), db: Session = Depends(get_db)):
    new_household = models.Household(name=name)
    db.add(new_household)
    db.commit()
    db.refresh(new_household)
    return new_household


# --- POLICY ENDPOINTS ---


@app.post("/policies/")
def create_policy(
    household_id: int = Form(...),  # NEW: Policies must belong to a household
    provider: str = Form(...),
    type: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    premium: float = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    file_location = None
    if file:
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_location = f"{upload_folder}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

    db_policy = models.Policy(
        household_id=household_id,
        provider=provider,
        type=type,
        start_date=start_date,
        end_date=end_date,
        premium=premium,
        document_path=file_location,
    )
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy


@app.get("/policies/")
def read_policies(household_id: Optional[int] = None, db: Session = Depends(get_db)):
    # If household_id is provided, filter by it. Otherwise return all (for now)
    query = db.query(models.Policy)
    if household_id:
        query = query.filter(models.Policy.household_id == household_id)
    return query.all()
