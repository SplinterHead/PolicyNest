# --- HOUSEHOLD ENDPOINTS ---
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from sqlalchemy import select

from app import models, schemas
from app.database import SessionDep
from app.uploads import delete_upload_file

router = APIRouter()


@router.get("/", response_model=list[schemas.HouseholdResponse])
def read_households(db: SessionDep) -> list[models.Household]:
    """List all households for the switcher menu."""
    return list(db.scalars(select(models.Household)).all())


@router.post("/", response_model=schemas.HouseholdResponse)
def create_household(
    data: Annotated[schemas.HouseholdForm, Form()],
    db: SessionDep,
) -> models.Household:
    """Create a new household."""
    new_household = models.Household(name=data.name)
    db.add(new_household)
    db.commit()
    db.refresh(new_household)
    return new_household


@router.delete("/{household_id}", response_model=schemas.DeleteResponse)
def delete_household(
    household_id: int,
    db: SessionDep,
) -> schemas.DeleteResponse:
    """Delete a household along with its associated policies, assets, and documents."""
    household = db.get(models.Household, household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    policies = db.scalars(
        select(models.Policy).where(models.Policy.household_id == household_id)
    ).all()
    for policy in policies:
        delete_upload_file(policy.document_path)

    db.delete(household)
    db.commit()
    return schemas.DeleteResponse()
