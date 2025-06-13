from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ConstructionStaticRow
from app.schemas import ConstructionStaticRowCreate, ConstructionStaticRowUpdate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/static-rows", response_class=HTMLResponse)
def static_rows_index(request: Request):
    """Main page for managing static rows."""
    return templates.TemplateResponse("static_rows/index.html", {"request": request})


@router.get("/static-rows/list", response_class=HTMLResponse)
def static_rows_list(request: Request, db: Session = Depends(get_db)):
    """Return the table body for the current static rows."""
    rows = db.query(ConstructionStaticRow).order_by(ConstructionStaticRow.id).all()
    return templates.TemplateResponse(
        "static_rows/partials/row_list.html",
        {"request": request, "rows": rows},
    )


@router.get("/static-rows/create", response_class=HTMLResponse)
def static_rows_create_form(request: Request):
    """Return an empty form for creating a new static row."""
    return templates.TemplateResponse(
        "static_rows/partials/form.html",
        {"request": request, "action": "/static-rows/create", "row": None},
    )


@router.post("/static-rows/create", response_class=HTMLResponse)
def static_rows_create(
    request: Request,
    resource: str = Form(...),
    flow_type: str = Form(...),
    fiscal_year: str = Form(...),
    flow_source: str = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db),
):
    """Handle form submission to create a new static row and return its table row HTML."""
    data = ConstructionStaticRowCreate(
        resource=resource,
        flow_type=flow_type,
        fiscal_year=fiscal_year,
        flow_source=flow_source,
        amount=amount,
    )
    row = ConstructionStaticRow(**data.dict())
    db.add(row)
    db.commit()
    db.refresh(row)
    return templates.TemplateResponse(
        "static_rows/partials/row_list.html",
        {"request": request, "rows": [row]},
    )


@router.get("/static-rows/{row_id}/edit", response_class=HTMLResponse)
def static_rows_edit_form(row_id: int, request: Request, db: Session = Depends(get_db)):
    """Return a form pre-filled for editing an existing static row."""
    row = db.query(ConstructionStaticRow).filter(ConstructionStaticRow.id == row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Static row not found")
    return templates.TemplateResponse(
        "static_rows/partials/form.html",
        {"request": request, "action": f"/static-rows/{row_id}/edit", "row": row},
    )


@router.post("/static-rows/{row_id}/edit", response_class=HTMLResponse)
def static_rows_edit(
    row_id: int,
    request: Request,
    resource: str = Form(...),
    flow_type: str = Form(...),
    fiscal_year: str = Form(...),
    flow_source: str = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db),
):
    """Handle form submission to update an existing static row and return its updated table row HTML."""
    row = db.query(ConstructionStaticRow).filter(ConstructionStaticRow.id == row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Static row not found")
    data = ConstructionStaticRowUpdate(
        resource=resource,
        flow_type=flow_type,
        fiscal_year=fiscal_year,
        flow_source=flow_source,
        amount=amount,
    )
    for field, value in data.dict().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return templates.TemplateResponse(
        "static_rows/partials/row_list.html",
        {"request": request, "rows": [row]},
    )


@router.delete("/static-rows/{row_id}", response_class=Response)
def static_rows_delete(row_id: int, db: Session = Depends(get_db)):
    """Handle deletion of a static row and return a 204 status to remove its row."""
    row = db.query(ConstructionStaticRow).filter(ConstructionStaticRow.id == row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Static row not found")
    db.delete(row)
    db.commit()
    return Response(status_code=204)