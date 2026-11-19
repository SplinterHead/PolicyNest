from datetime import date
from typing import Any

from sqlalchemy import JSON, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Household(Base):
    """Household grouping assets and insurance policies."""

    __tablename__ = "households"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)

    policies: Mapped[list["Policy"]] = relationship(
        back_populates="household", cascade="all, delete-orphan"
    )
    assets: Mapped[list["Asset"]] = relationship(
        back_populates="household", cascade="all, delete-orphan"
    )


class Asset(Base):
    """Insurable asset (such as a vehicle or pet) belonging to a household."""

    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    household_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("households.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    household: Mapped["Household"] = relationship(back_populates="assets")
    policies: Mapped[list["Policy"]] = relationship(back_populates="asset")


class Policy(Base):
    """Insurance policy record belonging to a household and optionally an asset."""

    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    household_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("households.id"), nullable=False
    )
    asset_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("assets.id"), nullable=True
    )
    provider: Mapped[str] = mapped_column(String, index=True, nullable=False)
    policy_number: Mapped[str | None] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    premium: Mapped[float] = mapped_column(Float, nullable=False)
    attributes: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    document_path: Mapped[str | None] = mapped_column(String, nullable=True)

    household: Mapped["Household"] = relationship(back_populates="policies")
    asset: Mapped["Asset | None"] = relationship(back_populates="policies")
