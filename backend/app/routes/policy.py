# --- POLICY ENDPOINTS ---
import json
import os
import shutil
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.uploads import save_upload_file

router = APIRouter()


@router.post("/")
def create_policy(
    household_id: int = Form(...),
    asset_id: Optional[int] = Form(None),
    provider: str = Form(...),
    policy_number: str = Form(...),
    type: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(None),
    premium: float = Form(...),
    attributes: str = Form("{}"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    file_location = None
    if file:
        file_location = save_upload_file(file)
        print(f"file location: {file_location}")

    parsed_attributes = json.loads(attributes)

    db_policy = models.Policy(
        household_id=household_id,
        asset_id=asset_id,
        provider=provider,
        policy_number=policy_number,
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


@router.get("/")
def read_policies(household_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Policy)
    if household_id:
        query = query.filter(models.Policy.household_id == household_id)
    return query.all()


@router.put("/{policy_id}/document")
def update_policy_document(
    policy_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    file_location = save_upload_file(file)

    policy.document_path = file_location
    db.commit()
    db.refresh(policy)
    return policy


@router.delete("/{policy_id}")
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    if policy.document_path and os.path.exists(policy.document_path):
        os.remove(policy.document_path)

    db.delete(policy)
    db.commit()
    return {"ok": True}


@router.put("/{policy_id}")
def update_policy(
    policy_id: int,
    household_id: int = Form(...),
    asset_id: Optional[int] = Form(None),
    provider: str = Form(...),
    policy_number: str = Form(...),
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
    policy.policy_number = policy_number
    policy.type = type
    policy.start_date = start_date
    policy.end_date = end_date
    policy.premium = premium
    policy.attributes = json.loads(attributes)

    db.commit()
    db.refresh(policy)
    return policy
