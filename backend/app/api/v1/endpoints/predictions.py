"""Location flood-risk prediction endpoints."""

from fastapi import APIRouter, Query, HTTPException, status
from app.schemas.schemas import PredictionResponse, PredictionQueryRequest
from app.core.config import settings
from app.core.exceptions import LocationOutOfBoundsException
from ml.inference import predict_location_risk

router = APIRouter()


def _validate_bounds(lat: float, lon: float):
    if not (
        settings.STUDY_AREA_MIN_LAT <= lat <= settings.STUDY_AREA_MAX_LAT
        and settings.STUDY_AREA_MIN_LON <= lon <= settings.STUDY_AREA_MAX_LON
    ):
        raise LocationOutOfBoundsException(lat, lon)


@router.get("/query", response_model=PredictionResponse, tags=["Predictions"])
def query_location_risk_get(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees"),
    lon: float = Query(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees"),
    target_type: str = Query("SUSCEPTIBILITY", description="SUSCEPTIBILITY or SHORT_HORIZON_FORECAST"),
    horizon_hours: int = Query(1, ge=1, le=24, description="Forecast horizon in hours"),
):
    """Inspect hyperlocal flood risk at specific coordinates."""
    _validate_bounds(lat, lon)
    try:
        res = predict_location_risk(
            lat=lat,
            lon=lon,
            target_type=target_type,
            horizon_hours=horizon_hours,
            demo_mode=settings.DEMO_MODE,
        )
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}",
        )


@router.post("/query", response_model=PredictionResponse, tags=["Predictions"])
def query_location_risk_post(payload: PredictionQueryRequest):
    """POST request for inspecting flood risk at specific coordinates."""
    _validate_bounds(payload.latitude, payload.longitude)
    try:
        res = predict_location_risk(
            lat=payload.latitude,
            lon=payload.longitude,
            target_type=payload.target_type,
            horizon_hours=payload.horizon_hours or 1,
            demo_mode=settings.DEMO_MODE,
        )
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}",
        )
