import json
import os
import shutil
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
api_router = APIRouter(prefix="/api")

UPLOADS_DIR = "/data/uploads"

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)


app.mount(UPLOADS_DIR, StaticFiles(directory=UPLOADS_DIR), name="uploads")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API ENDPOINTS ---


@api_router.get("/system/status")
def get_system_status(db: Session = Depends(get_db)):
    """Checks if a household exists to determine if onboarding is needed."""
    household = db.query(models.Household).first()
    if household:
        return {"initialized": True, "household": household}
    return {"initialized": False, "household": None}


# --- HOUSEHOLD ENDPOINTS ---


@api_router.get("/households/")
def read_households(db: Session = Depends(get_db)):
    """List all households for the switcher menu."""
    return db.query(models.Household).all()


@api_router.post("/households/")
def create_household(name: str = Form(...), db: Session = Depends(get_db)):
    new_household = models.Household(name=name)
    db.add(new_household)
    db.commit()
    db.refresh(new_household)
    return new_household


@api_router.delete("/households/{household_id}")
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


# --- ASSET ENDPOINTS ---


@api_router.get("/assets/")
def read_assets(household_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Asset).filter(models.Asset.household_id == household_id).all()
    )


@api_router.post("/assets/")
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


@api_router.delete("/assets/{asset_id}")
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


# --- POLICY ENDPOINTS ---


@api_router.post("/policies/")
def create_policy(
    household_id: int = Form(...),
    asset_id: Optional[int] = Form(None),
    provider: str = Form(...),
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
        file_location = f"{UPLOADS_DIR}/{file.filename}"
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


@api_router.get("/policies/")
def read_policies(household_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Policy)
    if household_id:
        query = query.filter(models.Policy.household_id == household_id)
    return query.all()


@api_router.put("/policies/{policy_id}/document")
def update_policy_document(
    policy_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    file_location = f"{UPLOADS_DIR}/{file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    policy.document_path = file_location
    db.commit()
    db.refresh(policy)
    return policy


@api_router.delete("/policies/{policy_id}")
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    if policy.document_path and os.path.exists(policy.document_path):
        os.remove(policy.document_path)

    db.delete(policy)
    db.commit()
    return {"ok": True}


@api_router.put("/policies/{policy_id}")
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


app.include_router(api_router)

# --- FRONTEND ---
if os.path.exists("../frontend/dist"):
    app.mount(
        "/assets", StaticFiles(directory="../frontend/dist/assets"), name="assets"
    )

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api") or full_path.startswith("uploads"):
            raise HTTPException(status_code=404, detail="Not Found")

        return FileResponse("../frontend/dist/index.html")
