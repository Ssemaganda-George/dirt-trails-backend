# app/models/booking.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tour_id = Column(Integer, ForeignKey("tours.id"), nullable=False)
    guests = Column(Integer, default=1)
    total_price = Column(Float, default=0.0)
    status = Column(String, default="confirmed")  # confirmed, cancelled, pending
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # optional relationships (for queries)
    # user = relationship("User", backref="bookings")
    # tour = relationship("Tour", backref="bookings")
