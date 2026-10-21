"""SQLAlchemy ORM models for FloodCast AI."""

import uuid
from datetime import datetime, timezone
from typing import Optional, Any
from sqlalchemy import (
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StudyArea(Base):
    __tablename__ = "study_areas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    center_lat: Mapped[float] = mapped_column(Float, nullable=False)
    center_lon: Mapped[float] = mapped_column(Float, nullable=False)
    min_lat: Mapped[float] = mapped_column(Float, nullable=False)
    max_lat: Mapped[float] = mapped_column(Float, nullable=False)
    min_lon: Mapped[float] = mapped_column(Float, nullable=False)
    max_lon: Mapped[float] = mapped_column(Float, nullable=False)
    boundary_geojson: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)

    reports = relationship("CommunityReport", back_populates="study_area")
    road_segments = relationship("RoadSegment", back_populates="study_area")


class CommunityReport(Base):
    __tablename__ = "community_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    study_area_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("study_areas.id"), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    fuzzed_latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fuzzed_longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    observation_time: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    depth_range: Mapped[str] = mapped_column(String(50), nullable=False)
    road_passability: Mapped[str] = mapped_column(String(50), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(20), default="UNVERIFIED", nullable=False)
    consent_granted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    client_ip_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, onupdate=get_utc_now, nullable=False)

    study_area = relationship("StudyArea", back_populates="reports")
    reviews = relationship("ReportReview", back_populates="report", cascade="all, delete-orphan")


class ReportReview(Base):
    __tablename__ = "report_reviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    report_id: Mapped[str] = mapped_column(String(36), ForeignKey("community_reports.id"), nullable=False)
    reviewer_id: Mapped[str] = mapped_column(String(100), default="system-reviewer", nullable=False)
    decision: Mapped[str] = mapped_column(String(20), nullable=False)  # VERIFIED, REJECTED, DUPLICATE
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)

    report = relationship("CommunityReport", back_populates="reviews")


class FloodEvent(Base):
    __tablename__ = "flood_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    event_date: Mapped[str] = mapped_column(String(20), nullable=False)  # YYYY-MM-DD
    total_rainfall_mm: Mapped[float] = mapped_column(Float, nullable=False)
    peak_intensity_mm_h: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    affected_wards: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)

    observations = relationship("FloodObservation", back_populates="event", cascade="all, delete-orphan")


class FloodObservation(Base):
    __tablename__ = "flood_observations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    event_id: Mapped[str] = mapped_column(String(36), ForeignKey("flood_events.id"), nullable=False)
    location_name: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    water_depth_cm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    observation_source: Mapped[str] = mapped_column(String(50), default="MUNICIPAL_RECORD", nullable=False)
    confidence: Mapped[str] = mapped_column(String(20), default="HIGH", nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)

    event = relationship("FloodEvent", back_populates="observations")


class RoadSegment(Base):
    __tablename__ = "road_segments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    study_area_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("study_areas.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    highway_type: Mapped[str] = mapped_column(String(50), default="primary", nullable=False)
    is_subway: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    elevation_m: Mapped[float] = mapped_column(Float, nullable=False)
    historical_vulnerability: Mapped[str] = mapped_column(String(20), default="MODERATE", nullable=False)
    line_geojson: Mapped[Any] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)

    study_area = relationship("StudyArea", back_populates="road_segments")


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    version_tag: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)  # SUSCEPTIBILITY, SATELLITE_DETECTION, FORECAST
    parameters: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    artifact_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)

    evaluations = relationship("ModelEvaluation", back_populates="model_version", cascade="all, delete-orphan")


class ModelEvaluation(Base):
    __tablename__ = "model_evaluations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    model_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("model_versions.id"), nullable=False)
    split_type: Mapped[str] = mapped_column(String(50), nullable=False)  # SPATIAL_HOLDOUT, EVENT_HOLDOUT, TEMPORAL
    pr_auc: Mapped[float] = mapped_column(Float, nullable=False)
    brier_score: Mapped[float] = mapped_column(Float, nullable=False)
    precision_at_k: Mapped[float] = mapped_column(Float, nullable=False)
    recall_at_k: Mapped[float] = mapped_column(Float, nullable=False)
    metrics_detail: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now, nullable=False)

    model_version = relationship("ModelVersion", back_populates="evaluations")
