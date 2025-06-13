from fastapi import FastAPI
from app.routes.projection import router as projection_router
from app.routes.static_rows import router as static_rows_router
from app.routes.static_rows_ui import router as static_rows_ui_router
from app.routes.settings import router as settings_router
from app.routes.settings_ui import router as settings_ui_router

app = FastAPI(title="Construction Budget API", version="1.0.0")

# UI routes for static rows and settings management using HTMX
app.include_router(static_rows_ui_router)
app.include_router(settings_ui_router)

# JSON API routes
app.include_router(projection_router, prefix="/api", tags=["projection"])
app.include_router(static_rows_router, prefix="/api", tags=["static_rows"])
app.include_router(settings_router, prefix="/api", tags=["settings"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)