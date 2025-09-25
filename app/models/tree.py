# app/models/tree.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db import Base

class Tree(Base):
    __tablename__ = "trees"
    id = Column(Integer, primary_key=True, index=True)
    species = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    planted_by = Column(String, nullable=True)  # could be user id or name
    planted_on = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(String, nullable=True)
