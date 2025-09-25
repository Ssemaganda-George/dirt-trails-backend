# app/routes/bookings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.booking import Booking
from app.models.tour import Tour
from app.schemas.booking import BookingCreate, BookingOut
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=BookingOut)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tour = db.query(Tour).filter(Tour.id == payload.tour_id, Tour.is_active == True).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    if payload.guests > tour.capacity:
        raise HTTPException(status_code=400, detail="Not enough capacity for requested guests")
    total_price = tour.price * payload.guests
    booking = Booking(user_id=current_user.id, tour_id=payload.tour_id, guests=payload.guests, total_price=total_price)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/me", response_model=list[BookingOut])
def my_bookings(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings

@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = "cancelled"
    db.commit()
    return {"ok": True, "booking_id": booking_id, "status": "cancelled"}
