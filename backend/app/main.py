from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import database, models
from .routes import asset, household, policy, system

FRONTEND_DIST = Path("../frontend/dist")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize storage directories and database tables on startup."""
    database.ensure_data_dirs()
    models.Base.metadata.create_all(bind=database.engine)
    yield


app = FastAPI(title="PolicyNest API", lifespan=lifespan)
app.mount(
    database.UPLOADS_MOUNT_PATH,
    StaticFiles(directory=database.UPLOADS_DIR, check_dir=False),
    name="uploads",
)

api_router = APIRouter(prefix="/api")
api_router.include_router(asset.router, prefix="/assets", tags=["assets"])
api_router.include_router(household.router, prefix="/households", tags=["households"])
api_router.include_router(policy.router, prefix="/policies", tags=["policies"])
api_router.include_router(system.router, prefix="/system", tags=["system"])

app.include_router(api_router)

# --- FRONTEND ---
if FRONTEND_DIST.exists():
    dist_root = FRONTEND_DIST.resolve()
    app.mount("/assets", StaticFiles(directory=dist_root / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api") or full_path.startswith("uploads"):
            raise HTTPException(status_code=404, detail="Not Found")

        if full_path:
            candidate = (dist_root / full_path).resolve()
            if candidate.is_relative_to(dist_root) and candidate.is_file():
                return FileResponse(
                    candidate,
                    headers={"Cache-Control": "public, max-age=86400"},
                )

        return FileResponse(dist_root / "index.html")
