# --- ASSET ENDPOINTS ---
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from sqlalchemy import select

from app import models, schemas
from app.database import SessionDep
from app.uploads import delete_upload_file

router = APIRouter()


@router.get("/", response_model=list[schemas.AssetResponse])
def read_assets(household_id: int, db: SessionDep) -> list[models.Asset]:
    """List all assets belonging to a household."""
    return list(
        db.scalars(
            select(models.Asset).where(models.Asset.household_id == household_id)
        ).all()
    )


@router.post("/", response_model=schemas.AssetResponse)
def create_asset(
    data: Annotated[schemas.AssetForm, Form()],
    db: SessionDep,
) -> models.Asset:
    """Create a new asset."""
    db_asset = models.Asset(**data.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.delete("/{asset_id}", response_model=schemas.DeleteResponse)
def delete_asset(asset_id: int, db: SessionDep) -> schemas.DeleteResponse:
    """Delete an asset and any policies attached to it."""
    asset = db.get(models.Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    policies = db.scalars(
        select(models.Policy).where(models.Policy.asset_id == asset_id)
    ).all()
    for policy in policies:
        delete_upload_file(policy.document_path)
        db.delete(policy)

    db.delete(asset)
    db.commit()
    return schemas.DeleteResponse()
