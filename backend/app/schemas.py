from datetime import date
from typing import Any, Dict, Optional

from pydantic import BaseModel


# ---------------------------------------------------------
# ASSETS (Vehicles, Homes, etc.)
# ---------------------------------------------------------
class AssetBase(BaseModel):
    name: str
    type: str
    household_id: int
    value: Optional[float] = 0.0


class AssetCreate(AssetBase):
    pass


class Asset(AssetBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------------------------------------
# POLICIES
# ---------------------------------------------------------
class PolicyBase(BaseModel):
    provider: str
    type: str
    premium: float
    frequency: Optional[str] = "Annual"
    start_date: date
    end_date: Optional[date] = None
    household_id: int
    asset_id: Optional[int] = None

    attributes: Optional[Dict[str, Any]] = {}


class PolicyCreate(PolicyBase):
    pass


class Policy(PolicyBase):
    id: int
    document_path: Optional[str] = None
    asset: Optional[Asset] = None

    class Config:
        from_attributes = True


# ---------------------------------------------------------
# HOUSEHOLDS
# ---------------------------------------------------------
class HouseholdBase(BaseModel):
    name: str


class HouseholdCreate(HouseholdBase):
    pass


class Household(HouseholdBase):
    id: int

    class Config:
        from_attributes = True
