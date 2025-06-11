from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models import ConstructionStaticRow
from app.schemas import ConstructionStaticRowCreate, ConstructionStaticRowUpdate, ConstructionStaticRowRead

router = APIRouter()

@router.get("/static-rows/", response_model=List[ConstructionStaticRowRead])
def read_static_rows(db: Session = Depends(get_db)):
    return db.query(ConstructionStaticRow).all()

@router.get("/static-rows/{row_id}", response_model=ConstructionStaticRowRead)
def get_static_row(row_id: int, db: Session = Depends(get_db)):
    row = db.query(ConstructionStaticRow).filter(ConstructionStaticRow.id == row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Static row not found")
    return row

@router.post("/static-rows/", response_model=ConstructionStaticRowRead)
def create_static_row(data: ConstructionStaticRowCreate, db: Session = Depends(get_db)):
    row = ConstructionStaticRow(**data.dict())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.put("/static-rows/{row_id}", response_model=ConstructionStaticRowRead)
def update_static_row(row_id: int, data: ConstructionStaticRowUpdate, db: Session = Depends(get_db)):
    row = db.query(ConstructionStaticRow).filter(ConstructionStaticRow.id == row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Static row not found")
    for field, value in data.dict().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row

@router.delete("/static-rows/{row_id}", response_model=dict)
def delete_static_row(row_id: int, db: Session = Depends(get_db)):
    row = db.query(ConstructionStaticRow).filter(ConstructionStaticRow.id == row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Static row not found")
    db.delete(row)
    db.commit()
    return {"message": "Row deleted"}
