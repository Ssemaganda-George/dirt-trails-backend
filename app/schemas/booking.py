# app/schemas/booking.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    tour_id: int
    guests: int = 1

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
