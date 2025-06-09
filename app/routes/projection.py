from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.projection import run_projection
from app.config import PASSPHRASE

router = APIRouter()

@router.post("/projection/run")
def run_construction_projection(passphrase: str, db: Session = Depends(get_db)):
    if passphrase != PASSPHRASE:
        return {"error": "Invalid passphrase"}
    status = run_projection(db)
    return {"status": status}