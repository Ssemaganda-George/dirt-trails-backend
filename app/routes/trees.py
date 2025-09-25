# app/routes/trees.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.tree import Tree
from app.schemas.tree import TreeCreate, TreeOut
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TreeOut)
def plant_tree(payload: TreeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tree = Tree(
        species=payload.species,
        latitude=payload.latitude,
        longitude=payload.longitude,
        planted_by=payload.planted_by or getattr(current_user, "full_name", current_user.email),
        notes=payload.notes
    )
    db.add(tree)
    db.commit()
    db.refresh(tree)
    return tree

@router.get("/", response_model=List[TreeOut])
def list_trees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trees = db.query(Tree).offset(skip).limit(limit).all()
    return trees

@router.get("/{tree_id}", response_model=TreeOut)
def get_tree(tree_id: int, db: Session = Depends(get_db)):
    t = db.query(Tree).filter(Tree.id == tree_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tree not found")
    return t
