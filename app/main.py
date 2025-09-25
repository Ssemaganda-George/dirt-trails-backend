# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, tours, bookings, trees
from app.db import engine, Base
import os

app = FastAPI(
    title="DirtTrails Safaris API",
    description="Backend for sustainable eco-tourism platform",
    version="1.0.0"
)

# CORS - allow your frontend origin (adjust for production)
origins = [
    "http://localhost:8081",
    "http://localhost:5173",
    "http://localhost:3000",
    "https://www.dirt-trails.com",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tours.router, prefix="/tours", tags=["Tours"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
app.include_router(trees.router, prefix="/trees", tags=["Conservation"])

@app.on_event("startup")
def on_startup():
    # create tables (use Alembic in production for migrations)
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome to DirtTrails Safaris API"}
