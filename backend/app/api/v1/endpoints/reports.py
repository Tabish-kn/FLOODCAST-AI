"""Community flood reports and moderation endpoints."""

import random
import hashlib
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import CommunityReport, ReportReview, StudyArea
from app.schemas.schemas import (
    CommunityReportCreate,
    CommunityReportReview,
    CommunityReportResponse,
)
from app.core.config import settings
from app.core.exceptions import LocationOutOfBoundsException, ResourceNotFoundException

router = APIRouter()


@router.post("", response_model=CommunityReportResponse, status_code=status.HTTP_201_CREATED, tags=["Reports"])
def submit_community_report(
    payload: CommunityReportCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Submits a new ground-truth flood report from citizens or delivery personnel.
    Always creates as UNVERIFIED until reviewed by authorized moderators.
    Applies ~50m location fuzzing if marked residential.
    """
    # 1. Bounds check
    if not (
        settings.STUDY_AREA_MIN_LAT <= payload.latitude <= settings.STUDY_AREA_MAX_LAT
        and settings.STUDY_AREA_MIN_LON <= payload.longitude <= settings.STUDY_AREA_MAX_LON
    ):
        raise LocationOutOfBoundsException(payload.latitude, payload.longitude)

    # 2. Location fuzzing for residential privacy
    fuzzed_lat = payload.latitude
    fuzzed_lon = payload.longitude
    if payload.is_residential:
        # ~50 meters is ~0.00045 degrees
        fuzzed_lat += random.uniform(-0.00045, 0.00045)
        fuzzed_lon += random.uniform(-0.00045, 0.00045)

    # 3. Anonymized IP hash
    client_ip = request.client.host if request.client else "unknown"
    ip_hash = hashlib.sha256(f"{client_ip}-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}".encode()).hexdigest()[:16]

    # Find study area
    study_area = db.query(StudyArea).first()
    study_area_id = study_area.id if study_area else None

    report = CommunityReport(
        study_area_id=study_area_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        fuzzed_latitude=fuzzed_lat,
        fuzzed_longitude=fuzzed_lon,
        observation_time=datetime.now(timezone.utc),
        category=payload.category,
        depth_range=payload.depth_range,
        road_passability=payload.road_passability,
        image_url=payload.image_url,
        verification_status="UNVERIFIED",
        consent_granted=payload.consent_granted,
        client_ip_hash=ip_hash,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


@router.get("", response_model=List[CommunityReportResponse], tags=["Reports"])
def list_community_reports(
    status_filter: Optional[str] = Query("ALL", description="ALL, VERIFIED, UNVERIFIED, REJECTED"),
    category: Optional[str] = Query(None, description="Filter by report category"),
    db: Session = Depends(get_db),
):
    """Lists community reports with optional status and category filters."""
    query = db.query(CommunityReport)

    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(CommunityReport.verification_status == status_filter.upper())

    if category:
        query = query.filter(CommunityReport.category == category)

    reports = query.order_by(CommunityReport.created_at.desc()).limit(100).all()
    return reports


@router.get("/{report_id}", response_model=CommunityReportResponse, tags=["Reports"])
def get_report_detail(report_id: str, db: Session = Depends(get_db)):
    """Retrieve details for a single community report."""
    report = db.query(CommunityReport).filter(CommunityReport.id == report_id).first()
    if not report:
        raise ResourceNotFoundException("CommunityReport", report_id)
    return report


@router.post("/{report_id}/review", response_model=CommunityReportResponse, tags=["Reports"])
def review_community_report(
    report_id: str,
    payload: CommunityReportReview,
    db: Session = Depends(get_db),
):
    """
    Moderator endpoint to verify, reject, or mark a report as duplicate.
    Updates report status and records audit log.
    """
    report = db.query(CommunityReport).filter(CommunityReport.id == report_id).first()
    if not report:
        raise ResourceNotFoundException("CommunityReport", report_id)

    report.verification_status = payload.decision
    report.notes = payload.reason
    report.updated_at = datetime.now(timezone.utc)

    review_log = ReportReview(
        report_id=report.id,
        reviewer_id=payload.reviewer_id or "authorized-reviewer",
        decision=payload.decision,
        reason=payload.reason,
    )

    db.add(review_log)
    db.commit()
    db.refresh(report)

    return report
