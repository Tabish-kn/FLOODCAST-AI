"""SQLAlchemy ORM models for FloodCast AI."""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class StudyArea(Base):
    __tablename__ = "study_areas"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, unique=True)
    center_lat = Column(Float, nullable=False)
    center_lon = Column(Float, nullable=False)
    min_lat = Column(Float, nullable=False)
    max_lat = Column(Float, nullable=False)
    min_lon = Column(Float, nullable=False)
    max_lon = Column(Float, nullable=False)
    boundary_geojson = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    reports = relationship("CommunityReport", back_populates="study_area")
    road_segments = relationship("RoadSegment", back_populates="study_area")


class CommunityReport(Base):
    __tablename__ = "community_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    study_area_id = Column(String(36), ForeignKey("study_areas.id"), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    fuzzed_latitude = Column(Float, nullable=True)
    fuzzed_longitude = Column(Float, nullable=True)
    observation_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    category = Column(String(50), nullable=False)
    depth_range = Column(String(50), nullable=False)
    road_passability = Column(String(50), nullable=False)
    image_url = Column(String(500), nullable=True)
    verification_status = Column(String(20), default="UNVERIFIED", nullable=False)
    consent_granted = Column(Boolean, default=False, nullable=False)
    client_ip_hash = Column(String(64), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    study_area = relationship("StudyArea", back_populates="reports")
    reviews = relationship("ReportReview", back_populates="report", cascade="all, delete-orphan")


class ReportReview(Base):
    __tablename__ = "report_reviews"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("community_reports.id"), nullable=False)
    reviewer_id = Column(String(100), default="system-reviewer", nullable=False)
    decision = Column(String(20), nullable=False)  # VERIFIED, REJECTED, DUPLICATE
    reason = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    report = relationship("CommunityReport", back_populates="reviews")


class FloodEvent(Base):
    __tablename__ = "flood_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    event_date = Column(String(20), nullable=False)  # YYYY-MM-DD
    total_rainfall_mm = Column(Float, nullable=False)
    peak_intensity_mm_h = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    affected_wards = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    observations = relationship("FloodObservation", back_populates="event", cascade="all, delete-orphan")


class FloodObservation(Base):
    __tablename__ = "flood_observations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("flood_events.id"), nullable=False)
    location_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    water_depth_cm = Column(Float, nullable=True)
    observation_source = Column(String(50), default="MUNICIPAL_RECORD", nullable=False)
    confidence = Column(String(20), default="HIGH", nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    event = relationship("FloodEvent", back_populates="observations")


class RoadSegment(Base):
    __tablename__ = "road_segments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    study_area_id = Column(String(36), ForeignKey("study_areas.id"), nullable=True)
    name = Column(String(100), nullable=False)
    highway_type = Column(String(50), default="primary", nullable=False)
    is_subway = Column(Boolean, default=False, nullable=False)
    elevation_m = Column(Float, nullable=False)
    historical_vulnerability = Column(String(20), default="MODERATE", nullable=False)
    line_geojson = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    study_area = relationship("StudyArea", back_populates="road_segments")


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    model_name = Column(String(100), nullable=False)
    version_tag = Column(String(50), nullable=False, unique=True)
    target_type = Column(String(50), nullable=False)  # SUSCEPTIBILITY, SATELLITE_DETECTION, FORECAST
    parameters = Column(JSON, nullable=True)
    artifact_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    evaluations = relationship("ModelEvaluation", back_populates="model_version", cascade="all, delete-orphan")


class ModelEvaluation(Base):
    __tablename__ = "model_evaluations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    model_version_id = Column(String(36), ForeignKey("model_versions.id"), nullable=False)
    split_type = Column(String(50), nullable=False)  # SPATIAL_HOLDOUT, EVENT_HOLDOUT, TEMPORAL
    pr_auc = Column(Float, nullable=False)
    brier_score = Column(Float, nullable=False)
    precision_at_k = Column(Float, nullable=False)
    recall_at_k = Column(Float, nullable=False)
    metrics_detail = Column(JSON, nullable=True)
    evaluated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    model_version = relationship("ModelVersion", back_populates="evaluations")
