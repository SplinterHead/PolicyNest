# --- POLICY ENDPOINTS ---
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from sqlalchemy import select

from app import models, schemas
from app.database import SessionDep
from app.uploads import delete_upload_file, save_upload_file

router = APIRouter()


@router.post("/", response_model=schemas.PolicyResponse)
def create_policy(
    data: Annotated[schemas.PolicyForm, Form()],
    db: SessionDep,
    file: Annotated[UploadFile | None, File()] = None,
) -> models.Policy:
    """Create a new insurance policy with an optional PDF document."""
    file_location = save_upload_file(file) if file else None

    db_policy = models.Policy(**data.model_dump(), document_path=file_location)
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy


@router.get("/", response_model=list[schemas.PolicyResponse])
def read_policies(
    db: SessionDep,
    household_id: int | None = None,
) -> list[models.Policy]:
    """List policies, optionally filtered by household."""
    stmt = select(models.Policy)
    if household_id is not None:
        stmt = stmt.where(models.Policy.household_id == household_id)
    return list(db.scalars(stmt).all())


@router.put("/{policy_id}/document", response_model=schemas.PolicyResponse)
def update_policy_document(
    policy_id: int,
    file: Annotated[UploadFile, File()],
    db: SessionDep,
) -> models.Policy:
    """Upload or replace the PDF document attached to a policy."""
    policy = db.get(models.Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    old_path = policy.document_path
    policy.document_path = save_upload_file(file)
    db.commit()
    db.refresh(policy)
    delete_upload_file(old_path)
    return policy


@router.delete("/{policy_id}", response_model=schemas.DeleteResponse)
def delete_policy(policy_id: int, db: SessionDep) -> schemas.DeleteResponse:
    """Delete a policy and remove any uploaded document."""
    policy = db.get(models.Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    delete_upload_file(policy.document_path)
    db.delete(policy)
    db.commit()
    return schemas.DeleteResponse()


@router.put("/{policy_id}", response_model=schemas.PolicyResponse)
def update_policy(
    policy_id: int,
    data: Annotated[schemas.PolicyForm, Form()],
    db: SessionDep,
    file: Annotated[UploadFile | None, File()] = None,
) -> models.Policy:
    """Update an existing policy and optionally replace its attached document."""
    policy = db.get(models.Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    old_path: str | None = None
    if file:
        old_path = policy.document_path
        policy.document_path = save_upload_file(file)

    for field, value in data.model_dump().items():
        setattr(policy, field, value)

    db.commit()
    db.refresh(policy)
    if old_path:
        delete_upload_file(old_path)
    return policy
