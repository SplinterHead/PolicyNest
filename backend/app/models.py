from sqlalchemy import JSON, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    policies = relationship("Policy", back_populates="household")
    assets = relationship("Asset", back_populates="household")


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    details = Column(JSON, nullable=False, default={})

    household = relationship("Household", back_populates="assets")
    policies = relationship("Policy", back_populates="asset")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    provider = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    premium = Column(Float, nullable=False)
    attributes = Column(JSON, nullable=False, default={})
    document_path = Column(String, nullable=True)

    household = relationship("Household", back_populates="policies")
    asset = relationship("Asset", back_populates="policies")
