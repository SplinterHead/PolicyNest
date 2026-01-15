import json
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


@app.get("/households/")
def read_households(db: Session = Depends(get_db)):
    """List all households for the switcher menu."""
    return db.query(models.Household).all()


@app.post("/households/")
def create_household(name: str = Form(...), db: Session = Depends(get_db)):
    new_household = models.Household(name=name)
    db.add(new_household)
    db.commit()
    db.refresh(new_household)
    return new_household


# --- ASSET ENDPOINTS ---


@app.get("/assets/")
def read_assets(household_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Asset).filter(models.Asset.household_id == household_id).all()
    )


@app.post("/assets/")
def create_asset(
    household_id: int = Form(...),
    name: str = Form(...),
    type: str = Form(...),
    details: str = Form("{}"),  # JSON string
    db: Session = Depends(get_db),
):
    parsed_details = json.loads(details)
    db_asset = models.Asset(
        household_id=household_id, name=name, type=type, details=parsed_details
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


# --- POLICY ENDPOINTS ---


@app.post("/policies/")
def create_policy(
    household_id: int = Form(...),
    asset_id: Optional[int] = Form(None),
    provider: str = Form(...),
    type: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    premium: float = Form(...),
    attributes: str = Form("{}"),
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

    parsed_attributes = json.loads(attributes)

    db_policy = models.Policy(
        household_id=household_id,
        asset_id=asset_id,
        provider=provider,
        type=type,
        start_date=start_date,
        end_date=end_date,
        premium=premium,
        attributes=parsed_attributes,
        document_path=file_location,
    )

    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy


@app.get("/policies/")
def read_policies(household_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Policy)
    if household_id:
        query = query.filter(models.Policy.household_id == household_id)
    return query.all()


@app.put("/policies/{policy_id}/document")
def update_policy_document(
    policy_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_location = f"{upload_folder}/{file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    policy.document_path = file_location
    db.commit()
    db.refresh(policy)
    return policy


@app.delete("/policies/{policy_id}")
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    if policy.document_path and os.path.exists(policy.document_path):
        os.remove(policy.document_path)

    db.delete(policy)
    db.commit()
    return {"ok": True}


@app.put("/policies/{policy_id}")
def update_policy(
    policy_id: int,
    household_id: int = Form(...),
    asset_id: Optional[int] = Form(None),
    provider: str = Form(...),
    type: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    premium: float = Form(...),
    attributes: str = Form("{}"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    if file:
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_location = f"{upload_folder}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        policy.document_path = file_location

    policy.household_id = household_id
    policy.asset_id = asset_id
    policy.provider = provider
    policy.type = type
    policy.start_date = start_date
    policy.end_date = end_date
    policy.premium = premium
    policy.attributes = json.loads(attributes)

    db.commit()
    db.refresh(policy)
    return policy
