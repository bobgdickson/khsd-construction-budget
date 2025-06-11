from fastapi import FastAPI
from app.routes.projection import router as projection_router
from app.routes.static_rows import router as static_rows_router


app = FastAPI(title="Construction Budget API", version="1.0.0")

app.include_router(projection_router, prefix="/api", tags=["projection"])
app.include_router(static_rows_router, prefix="/api", tags=["static_rows"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)