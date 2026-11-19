# --- API ENDPOINTS ---
from fastapi import APIRouter
from sqlalchemy import select

from app import schemas
from app.database import SessionDep
from app.models import Household

router = APIRouter()


@router.get("/status", response_model=schemas.SystemStatusResponse)
def get_system_status(db: SessionDep) -> schemas.SystemStatusResponse:
    """Check if a household exists to determine if onboarding is needed."""
    household = db.scalar(select(Household).limit(1))
    return schemas.SystemStatusResponse(
        initialized=household is not None,
        household=household,
    )
