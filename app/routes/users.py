# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models.user import User
from app.schemas.user import Token
from app.auth import create_access_token
from app.auth_service import verify_google_token, verify_apple_token

router = APIRouter()

# --- Request schema ---
class OAuthLoginRequest(BaseModel):
    token: str

# --- Google OAuth login ---
@router.post("/login/google", response_model=Token)
def login_google(data: OAuthLoginRequest, db: Session = Depends(get_db)):
    user_data = verify_google_token(data.token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    user = db.query(User).filter(User.google_id == user_data["google_id"]).first()
    if not user:
        # Create new user
        user = User(
            email=user_data["email"],
            full_name=user_data.get("name"),
            google_id=user_data["google_id"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Apple OAuth login ---
@router.post("/login/apple", response_model=Token)
def login_apple(data: OAuthLoginRequest, db: Session = Depends(get_db)):
    user_data = verify_apple_token(data.token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Apple token")

    user = db.query(User).filter(User.apple_id == user_data["apple_id"]).first()
    if not user:
        # Create new user
        user = User(
            email=user_data["email"],
            full_name=user_data.get("name"),
            apple_id=user_data["apple_id"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
