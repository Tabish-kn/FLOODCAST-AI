"""Health, readiness, and metadata endpoints."""

import os
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["System"])
def health_check():
    """Liveness probe."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@router.get("/ready", tags=["System"])
def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe checking database and model availability."""
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        db_ok = False

    model_path = os.path.join(settings.DATA_DIR, "models", "baseline_rf_susceptibility.joblib")
    model_ok = os.path.exists(model_path) or os.path.exists("data/models/baseline_rf_susceptibility.joblib")

    is_ready = db_ok and model_ok
    return {
        "ready": is_ready,
        "database_connected": db_ok,
        "model_loaded": model_ok,
        "demo_mode": settings.DEMO_MODE,
        "study_area": settings.STUDY_AREA_NAME,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/metadata", tags=["System"])
def system_metadata():
    """System capabilities and operational metadata."""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "study_area": {
            "name": settings.STUDY_AREA_NAME,
            "center": [settings.STUDY_AREA_CENTER_LAT, settings.STUDY_AREA_CENTER_LON],
            "bounds": [
                [settings.STUDY_AREA_MIN_LAT, settings.STUDY_AREA_MIN_LON],
                [settings.STUDY_AREA_MAX_LAT, settings.STUDY_AREA_MAX_LON],
            ],
            "crs": "EPSG:4326 (WGS 84)",
            "metric_crs": "EPSG:32643 (UTM Zone 43N)",
        },
        "supported_targets": [
            "STATIC_SUSCEPTIBILITY",
            "HISTORICAL_EVENT_REPLAY",
            "COMMUNITY_REPORTS",
        ],
        "unsupported_targets_note": (
            "Live 1-6h convective nowcasting is active in demo mode using synthetic proxies; "
            "production radar requires verified municipal Doppler feeds."
        ),
        "demo_mode": settings.DEMO_MODE,
    }
