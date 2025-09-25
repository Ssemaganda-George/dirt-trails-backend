from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.models.tour import Tour
from app.schemas.tour import TourCreate, TourOut, TourUpdate

router = APIRouter()

@router.post("/", response_model=TourOut)
def create_tour(tour: TourCreate, db: Session = Depends(get_db)):
    exists = db.query(Tour).filter(Tour.slug == tour.slug).first()
    if exists:
        raise HTTPException(status_code=400, detail="Tour slug already exists")
    t = Tour(**tour.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

# UPDATED: Add filters for destination, days, and guests
@router.get("/", response_model=List[TourOut])
def list_tours(
    skip: int = 0,
    limit: int = 20,
    active: Optional[bool] = True,
    destination: Optional[str] = Query(None),
    days: Optional[int] = Query(None),
    guests: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    q = db.query(Tour)
    
    if active is not None:
        q = q.filter(Tour.is_active == active)
    
    if destination:
        q = q.filter(Tour.location.ilike(f"%{destination}%"))
    
    if days:
        q = q.filter(Tour.duration_days == days)
    
    if guests:
        q = q.filter(Tour.capacity >= guests)
    
    tours = q.offset(skip).limit(limit).all()
    return tours

@router.get("/{tour_id}", response_model=TourOut)
def get_tour(tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    return tour

@router.put("/{tour_id}", response_model=TourOut)
def update_tour(tour_id: int, tour_in: TourUpdate, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    for k, v in tour_in.dict(exclude_unset=True).items():
        setattr(tour, k, v)
    db.commit()
    db.refresh(tour)
    return tour

@router.delete("/{tour_id}")
def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    db.delete(tour)
    db.commit()
    return {"ok": True}
