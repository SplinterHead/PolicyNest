from sqlalchemy import Column, Date, Float, Integer, String

from .database import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, index=True)
    type = Column(String)  # e.g., Car, Life, Home
    start_date = Column(Date)
    end_date = Column(Date)
    premium = Column(Float)
    document_path = Column(String, nullable=True)  # Path to the uploaded PDF
