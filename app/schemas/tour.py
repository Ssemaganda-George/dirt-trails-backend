from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TourBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    location: Optional[str] = None
    price: float
    duration_days: int = 1
    capacity: int = 10
    is_active: bool = True

class TourCreate(TourBase):
    pass

class TourUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    duration_days: Optional[int]
    capacity: Optional[int]
    is_active: Optional[bool]

class TourOut(TourBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
