# --- HOUSEHOLD ENDPOINTS ---
import os

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

router = APIRouter()


@router.get("/")
def read_households(db: Session = Depends(get_db)):
    """List all households for the switcher menu."""
    return db.query(models.Household).all()


@router.post("/")
def create_household(name: str = Form(...), db: Session = Depends(get_db)):
    new_household = models.Household(name=name)
    db.add(new_household)
    db.commit()
    db.refresh(new_household)
    return new_household


@router.delete("/{household_id}")
def delete_household(household_id: int, db: Session = Depends(get_db)):
    household = (
        db.query(models.Household).filter(models.Household.id == household_id).first()
    )
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    policies = (
        db.query(models.Policy).filter(models.Policy.household_id == household_id).all()
    )
    for policy in policies:
        if policy.document_path and os.path.exists(policy.document_path):
            try:
                os.remove(policy.document_path)
            except Exception as e:
                print(f"Error deleting file {policy.document_path}: {e}")

    db.delete(household)
    db.commit()

    return {"ok": True}
