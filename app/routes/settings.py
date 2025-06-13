from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ConstructionSetting
from app.schemas import (
    ConstructionSettingCreate,
    ConstructionSettingUpdate,
    ConstructionSettingRead,
)

router = APIRouter()

@router.get("/settings/", response_model=List[ConstructionSettingRead])
def read_settings(db: Session = Depends(get_db)):
    return db.query(ConstructionSetting).all()

@router.get("/settings/{name}", response_model=ConstructionSettingRead)
def get_setting_item(name: str, db: Session = Depends(get_db)):
    setting = db.query(ConstructionSetting).filter(ConstructionSetting.name == name).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@router.post("/settings/", response_model=ConstructionSettingRead)
def create_setting(data: ConstructionSettingCreate, db: Session = Depends(get_db)):
    setting = ConstructionSetting(**data.dict())
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting

@router.put("/settings/{name}", response_model=ConstructionSettingRead)
def update_setting(name: str, data: ConstructionSettingUpdate, db: Session = Depends(get_db)):
    setting = db.query(ConstructionSetting).filter(ConstructionSetting.name == name).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting.value = data.value
    db.commit()
    db.refresh(setting)
    return setting

@router.delete("/settings/{name}", response_model=dict)
def delete_setting(name: str, db: Session = Depends(get_db)):
    setting = db.query(ConstructionSetting).filter(ConstructionSetting.name == name).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    db.delete(setting)
    db.commit()
    return {"message": "Setting deleted"}