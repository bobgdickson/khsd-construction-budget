from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.projection import run_projection
from app.config import PASSPHRASE

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/projection", response_class=HTMLResponse)
def projection_index(request: Request):
    """Main page for running multi-year construction budget projections."""
    return templates.TemplateResponse(
        "projection/index.html",
        {"request": request},
    )


@router.post("/projection/run", response_class=HTMLResponse)
def projection_run_ui(
    request: Request,
    passphrase: str = Form(...),
    db: Session = Depends(get_db),
):
    """Handle form submission to run projection and return the result."""
    if passphrase != PASSPHRASE:
        status = "Invalid passphrase"
        error = True
    else:
        status = run_projection(db)
        error = False
    return templates.TemplateResponse(
        "projection/partials/result.html",
        {"request": request, "status": status, "error": error},
    )