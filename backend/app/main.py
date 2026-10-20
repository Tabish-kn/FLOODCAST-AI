import sys
from pathlib import Path

# Add backend and repo root to sys.path
backend_path = Path(__file__).resolve().parent.parent
repo_root = backend_path.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import FloodCastException
from app.api.v1.api import api_router
from app.db.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-seed database if empty on startup
    try:
        seed_database()
    except Exception as e:
        print(f"[Startup] Database seed check encountered: {e}")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Hyperlocal Urban Flood-Risk Intelligence Platform (Mumbai Study Area)",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(FloodCastException)
async def floodcast_exception_handler(request: Request, exc: FloodCastException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


# Root health checks for monitoring probes
@app.get("/health", tags=["System"])
def root_health():
    return {"status": "healthy", "service": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/ready", tags=["System"])
def root_ready():
    return {"status": "ready", "study_area": settings.STUDY_AREA_NAME, "demo_mode": settings.DEMO_MODE}


# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
