from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, Json


class AssetForm(BaseModel):
    """Form payload for creating an asset."""

    household_id: int
    name: str
    type: str
    details: Json[dict[str, Any]] | dict[str, Any] = Field(default_factory=dict)


class AssetResponse(BaseModel):
    """Serialized asset returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    household_id: int
    name: str
    type: str
    details: dict[str, Any]


class PolicyForm(BaseModel):
    """Form payload for creating or updating a policy."""

    household_id: int
    asset_id: int | None = None
    provider: str
    policy_number: str | None = None
    type: str
    start_date: date
    end_date: date | None = None
    premium: float
    attributes: Json[dict[str, Any]] | dict[str, Any] = Field(default_factory=dict)


class PolicyResponse(BaseModel):
    """Serialized policy returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    household_id: int
    asset_id: int | None = None
    provider: str
    policy_number: str | None = None
    type: str
    start_date: date
    end_date: date | None = None
    premium: float
    attributes: dict[str, Any]
    document_path: str | None = None


class HouseholdForm(BaseModel):
    """Form payload for creating a household."""

    name: str


class HouseholdResponse(BaseModel):
    """Serialized household returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class SystemStatusResponse(BaseModel):
    """Initialization status response for onboarding checks."""

    initialized: bool
    household: HouseholdResponse | None = None


class DeleteResponse(BaseModel):
    """Standard acknowledgement returned by delete endpoints."""

    ok: bool = True
