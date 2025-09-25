# app/schemas/tree.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TreeCreate(BaseModel):
    species: str
    latitude: float
    longitude: float
    planted_by: Optional[str] = None
    notes: Optional[str] = None

class TreeOut(TreeCreate):
    id: int
    planted_on: datetime

    class Config:
        orm_mode = True
