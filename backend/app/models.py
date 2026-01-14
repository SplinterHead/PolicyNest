from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g. "The Smith Family"

    # Relationship to policies
    policies = relationship("Policy", back_populates="household")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"))  # Link to Household
    provider = Column(String, index=True)
    type = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    premium = Column(Float)
    document_path = Column(String, nullable=True)

    household = relationship("Household", back_populates="policies")
