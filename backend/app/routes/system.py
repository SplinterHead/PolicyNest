# --- API ENDPOINTS ---
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Household

router = APIRouter()


@router.get("/status")
def get_system_status(db: Session = Depends(get_db)):
    """Checks if a household exists to determine if onboarding is needed."""
    household = db.query(Household).first()
    if household:
        return {"initialized": True, "household": household}
    return {"initialized": False, "household": None}
