"""Pydantic schemas for request validation and response serialization."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


# -----------------------------------------------------------------------------
# Study Area Schemas
# -----------------------------------------------------------------------------
class StudyAreaResponse(BaseModel):
    id: str
    name: str
    center_lat: float
    center_lon: float
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
    boundary_geojson: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


# -----------------------------------------------------------------------------
# Community Report Schemas
# -----------------------------------------------------------------------------
class CommunityReportCreate(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    category: str = Field(..., description="Report category (e.g., WATERLOGGING, ROAD_IMPASSABLE, DRAIN_OVERFLOW)")
    depth_range: str = Field(..., description="Estimated depth range (e.g., <6 in, 6-12 in, 1-2 ft, >2 ft, UNKNOWN)")
    road_passability: str = Field(..., description="PASSABLE, TWO_WHEELERS_ONLY, HEAVY_ONLY, IMPASSABLE")
    image_url: Optional[str] = Field(None, description="Optional photo URL (EXIF stripped)")
    consent_granted: bool = Field(..., description="Explicit user consent for participatory mapping")
    is_residential: Optional[bool] = Field(False, description="Whether to apply ~50m location fuzzing for privacy")

    @field_validator("consent_granted")
    def validate_consent(cls, v: bool) -> bool:
        if not v:
            raise ValueError("You must provide consent for the report to be used for research and public hazard notification.")
        return v


class CommunityReportReview(BaseModel):
    decision: str = Field(..., description="VERIFIED, REJECTED, DUPLICATE")
    reason: Optional[str] = Field(None, description="Review reason or notes")
    reviewer_id: Optional[str] = Field("moderator-admin", description="Reviewer identifier")

    @field_validator("decision")
    def validate_decision(cls, v: str) -> str:
        valid = ["VERIFIED", "REJECTED", "DUPLICATE"]
        if v.upper() not in valid:
            raise ValueError(f"Decision must be one of {valid}")
        return v.upper()


class CommunityReportResponse(BaseModel):
    id: str
    latitude: float
    longitude: float
    observation_time: datetime
    category: str
    depth_range: str
    road_passability: str
    image_url: Optional[str] = None
    verification_status: str
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# -----------------------------------------------------------------------------
# Location Prediction & Risk Schemas
# -----------------------------------------------------------------------------
class PredictionQueryRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    target_type: str = Field("SUSCEPTIBILITY", description="SUSCEPTIBILITY or SHORT_HORIZON_FORECAST")
    horizon_hours: Optional[int] = Field(1, ge=1, le=24, description="Forecast horizon in hours (if forecast requested)")


class HydrologicalFeatures(BaseModel):
    elevation_m: float
    slope_degrees: float
    distance_to_waterway_m: float
    distance_to_storm_outfall_m: float
    impervious_surface_fraction: float
    historical_waterlogging_frequency: int
    is_depression: bool


class UncertaintyMeta(BaseModel):
    confidence_tier: str  # HIGH, MODERATE, LOW
    is_calibrated: bool
    data_freshness: str  # LIVE, STALE, DEMO_MODE
    missing_proxies: List[str]
    limitations_note: str


class PredictionResponse(BaseModel):
    prediction_id: str
    target_type: str
    latitude: float
    longitude: float
    risk_score: float  # Calibrated probability [0.0 - 1.0]
    risk_tier: str  # LOW, MODERATE, HIGH, CRITICAL
    issue_time: datetime
    target_window: str
    model_version: str
    features: HydrologicalFeatures
    supporting_observations_count: int
    nearby_subway_status: Optional[str] = None
    uncertainty: UncertaintyMeta
    demo_mode: bool


# -----------------------------------------------------------------------------
# Historical Flood Events Schemas
# -----------------------------------------------------------------------------
class FloodObservationResponse(BaseModel):
    id: str
    location_name: str
    latitude: float
    longitude: float
    water_depth_cm: Optional[float] = None
    observation_source: str
    confidence: str
    recorded_at: datetime

    model_config = {"from_attributes": True}


class FloodEventResponse(BaseModel):
    id: str
    name: str
    event_date: str
    total_rainfall_mm: float
    peak_intensity_mm_h: float
    description: Optional[str] = None
    observations: List[FloodObservationResponse] = []

    model_config = {"from_attributes": True}


# -----------------------------------------------------------------------------
# Road Segment Schemas
# -----------------------------------------------------------------------------
class RoadSegmentResponse(BaseModel):
    id: str
    name: str
    highway_type: str
    is_subway: bool
    elevation_m: float
    historical_vulnerability: str
    line_geojson: Dict[str, Any]

    model_config = {"from_attributes": True}


# -----------------------------------------------------------------------------
# Model Metrics Schemas
# -----------------------------------------------------------------------------
class ModelEvaluationResponse(BaseModel):
    id: str
    model_version_id: str
    split_type: str
    pr_auc: float
    brier_score: float
    precision_at_k: float
    recall_at_k: float
    metrics_detail: Optional[Dict[str, Any]] = None
    evaluated_at: datetime

    model_config = {"from_attributes": True}


class ModelVersionResponse(BaseModel):
    id: str
    model_name: str
    version_tag: str
    target_type: str
    parameters: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    evaluations: List[ModelEvaluationResponse] = []

    model_config = {"from_attributes": True}
