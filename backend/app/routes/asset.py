# --- ASSET ENDPOINTS ---
import json

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

router = APIRouter()


@router.get("/")
def read_assets(household_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Asset).filter(models.Asset.household_id == household_id).all()
    )


@router.post("/")
def create_asset(
    household_id: int = Form(...),
    name: str = Form(...),
    type: str = Form(...),
    details: str = Form("{}"),
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


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    policies = db.query(models.Policy).filter(models.Policy.asset_id == asset_id).all()
    for policy in policies:
        if policy.document_path and os.path.exists(policy.document_path):
            try:
                os.remove(policy.document_path)
            except Exception as e:
                print(f"Error deleting file {policy.document_path}: {e}")
    for p in policies:
        db.delete(p)

    db.delete(asset)
    db.commit()

    return {"ok": True}
