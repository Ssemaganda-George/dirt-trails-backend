from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.db import Base

class Tour(Base):
    __tablename__ = "tours"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)  # used as "destination" in filter
    price = Column(Float, nullable=False, default=0.0)
    duration_days = Column(Integer, default=1)  # used as "days" filter
    capacity = Column(Integer, default=10)      # used as "guests" filter
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
