import os

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import database, models
from .routes import asset, household, policy, system

UPLOADS_DIR = "/data/uploads"

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="PolicyNest API")
app.mount(UPLOADS_DIR, StaticFiles(directory=UPLOADS_DIR), name="uploads")

api_router = APIRouter(prefix="/api")
api_router.include_router(asset.router, prefix="/assets", tags=["assets"])
api_router.include_router(household.router, prefix="/households", tags=["households"])
api_router.include_router(policy.router, prefix="/policies", tags=["policies"])
api_router.include_router(system.router, prefix="/system", tags=["system"])

app.include_router(api_router)

# --- FRONTEND ---
if os.path.exists("../frontend/dist"):
    app.mount(
        "/assets", StaticFiles(directory="../frontend/dist/assets"), name="assets"
    )

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api") or full_path.startswith("uploads"):
            raise HTTPException(status_code=404, detail="Not Found")

        return FileResponse("../frontend/dist/index.html")
