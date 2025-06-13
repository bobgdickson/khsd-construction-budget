from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ConstructionSetting
from app.schemas import ConstructionSettingCreate, ConstructionSettingUpdate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/settings", response_class=HTMLResponse)
def settings_index(request: Request):
    """Main page for managing settings."""
    return templates.TemplateResponse("settings/index.html", {"request": request})


@router.get("/settings/list", response_class=HTMLResponse)
def settings_list(request: Request, db: Session = Depends(get_db)):
    """Return the table body for the current settings."""
    settings = db.query(ConstructionSetting).order_by(ConstructionSetting.name).all()
    return templates.TemplateResponse(
        "settings/partials/row_list.html",
        {"request": request, "settings": settings},
    )


@router.get("/settings/create", response_class=HTMLResponse)
def settings_create_form(request: Request):
    """Return an empty form for creating a new setting."""
    return templates.TemplateResponse(
        "settings/partials/form.html",
        {"request": request, "action": "/settings/create", "setting": None},
    )


@router.post("/settings/create", response_class=HTMLResponse)
def settings_create(
    request: Request,
    name: str = Form(...),
    value: str = Form(...),
    db: Session = Depends(get_db),
):
    """Handle form submission to create a new setting and return its table row HTML."""
    data = ConstructionSettingCreate(name=name, value=value)
    setting = ConstructionSetting(**data.dict())
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return templates.TemplateResponse(
        "settings/partials/row_list.html",
        {"request": request, "settings": [setting]},
    )


@router.get("/settings/{name}/edit", response_class=HTMLResponse)
def settings_edit_form(name: str, request: Request, db: Session = Depends(get_db)):
    """Return a form pre-filled for editing an existing setting."""
    setting = db.query(ConstructionSetting).filter(ConstructionSetting.name == name).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return templates.TemplateResponse(
        "settings/partials/form.html",
        {"request": request, "action": f"/settings/{name}/edit", "setting": setting},
    )


@router.post("/settings/{name}/edit", response_class=HTMLResponse)
def settings_edit(
    name: str,
    request: Request,
    value: str = Form(...),
    db: Session = Depends(get_db),
):
    """Handle form submission to update an existing setting and return its updated table row HTML."""
    setting = db.query(ConstructionSetting).filter(ConstructionSetting.name == name).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    data = ConstructionSettingUpdate(name=name, value=value)
    setting.value = data.value
    db.commit()
    db.refresh(setting)
    return templates.TemplateResponse(
        "settings/partials/row_list.html",
        {"request": request, "settings": [setting]},
    )


@router.delete("/settings/{name}", response_class=Response)
def settings_delete(name: str, db: Session = Depends(get_db)):
    """Handle deletion of a setting and return a 204 status to remove its row."""
    setting = db.query(ConstructionSetting).filter(ConstructionSetting.name == name).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    db.delete(setting)
    db.commit()
    return Response(status_code=204)