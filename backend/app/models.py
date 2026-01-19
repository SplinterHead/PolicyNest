from sqlalchemy import JSON, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    policies = relationship("Policy", back_populates="household")
    assets = relationship("Asset", back_populates="household")


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    name = Column(String)
    type = Column(String)
    details = Column(JSON, default={})

    household = relationship("Household", back_populates="assets")
    policies = relationship("Policy", back_populates="asset")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    provider = Column(String, index=True)
    type = Column(String)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    premium = Column(Float)
    attributes = Column(JSON, default={})
    document_path = Column(String, nullable=True)

    household = relationship("Household", back_populates="policies")
    asset = relationship("Asset", back_populates="policies")
