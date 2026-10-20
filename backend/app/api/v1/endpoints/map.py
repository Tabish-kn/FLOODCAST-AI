"""Map layers and geospatial features endpoints."""

import os
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from app.db.session import get_db
from app.models.entities import StudyArea, RoadSegment, CommunityReport, FloodObservation
from app.schemas.schemas import StudyAreaResponse, RoadSegmentResponse
from app.core.config import settings

router = APIRouter()

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
GRID_FIXTURE_PATH = REPO_ROOT / "data" / "fixtures" / "mumbai_susceptibility_grid.geojson"



@router.get("/study-areas", response_model=List[StudyAreaResponse], tags=["Map"])
def list_study_areas(db: Session = Depends(get_db)):
    """Returns active study areas."""
    return db.query(StudyArea).all()


@router.get("/layers", tags=["Map"])
def list_map_layers():
    """Returns registry of available geospatial layers, status, and freshness."""
    return {
        "layers": [
            {
                "id": "flood_susceptibility",
                "name": "Static Flood Susceptibility",
                "category": "MODEL_PREDICTION",
                "status": "AVAILABLE",
                "description": "Calibrated Random Forest baseline model based on Mumbai topography, slope, and coastal outfalls.",
                "geometry_type": "Polygon",
                "freshness": "STATIC_BASELINE_V1",
                "is_default_visible": True,
            },
            {
                "id": "road_corridors",
                "name": "Road Corridors & Underpasses",
                "category": "INFRASTRUCTURE",
                "status": "AVAILABLE",
                "description": "Major transport arteries and critical subways (Milan, Andheri, Malad) with flood vulnerability flags.",
                "geometry_type": "LineString",
                "freshness": "OSM_VERIFIED",
                "is_default_visible": True,
            },
            {
                "id": "community_reports",
                "name": "Community Flood Reports",
                "category": "PARTICIPATORY",
                "status": "AVAILABLE",
                "description": "Ground observations submitted by citizens and field delivery personnel (Verified & Pending).",
                "geometry_type": "Point",
                "freshness": "REALTIME",
                "is_default_visible": True,
            },
            {
                "id": "historical_hotspots",
                "name": "Historical Flood Observations",
                "category": "HISTORICAL",
                "status": "AVAILABLE",
                "description": "Documented waterlogging records from major Mumbai monsoon deluge events (2005, 2017, 2021, 2023).",
                "geometry_type": "Point",
                "freshness": "ARCHIVAL",
                "is_default_visible": False,
            },
            {
                "id": "satellite_inundation",
                "name": "Sentinel-1 SAR Inundation",
                "category": "REMOTE_SENSING",
                "status": "UNAVAILABLE",
                "description": "Synthetic Aperture Radar water backscatter change. Currently awaiting Copernicus Data Space pipeline connection.",
                "geometry_type": "Raster",
                "freshness": "PENDING_SENSOR",
                "is_default_visible": False,
            },
        ]
    }


@router.get("/features", tags=["Map"])
def get_map_features(
    layer: str = Query("susceptibility", description="susceptibility, roads, reports, or observations"),
    db: Session = Depends(get_db),
):
    """Returns GeoJSON FeatureCollection for the requested layer."""
    if layer == "susceptibility":
        if os.path.exists(GRID_FIXTURE_PATH):
            with open(GRID_FIXTURE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            raise HTTPException(status_code=404, detail="Susceptibility grid fixture not found.")

    elif layer == "roads":
        roads = db.query(RoadSegment).all()
        features = []
        for r in roads:
            features.append({
                "type": "Feature",
                "id": r.id,
                "geometry": r.line_geojson,
                "properties": {
                    "id": r.id,
                    "name": r.name,
                    "highway_type": r.highway_type,
                    "is_subway": r.is_subway,
                    "elevation_m": r.elevation_m,
                    "historical_vulnerability": r.historical_vulnerability,
                },
            })
        return {
            "type": "FeatureCollection",
            "name": "Mumbai Critical Road Segments",
            "features": features,
        }

    elif layer == "reports":
        reports = db.query(CommunityReport).filter(CommunityReport.verification_status != "REJECTED").all()
        features = []
        for rep in reports:
            features.append({
                "type": "Feature",
                "id": rep.id,
                "geometry": {
                    "type": "Point",
                    "coordinates": [rep.fuzzed_longitude or rep.longitude, rep.fuzzed_latitude or rep.latitude],
                },
                "properties": {
                    "id": rep.id,
                    "category": rep.category,
                    "depth_range": rep.depth_range,
                    "road_passability": rep.road_passability,
                    "verification_status": rep.verification_status,
                    "observation_time": rep.observation_time.isoformat(),
                    "notes": rep.notes,
                },
            })
        return {
            "type": "FeatureCollection",
            "name": "Mumbai Community Flood Reports",
            "features": features,
        }

    elif layer == "observations":
        obs = db.query(FloodObservation).all()
        features = []
        for o in obs:
            features.append({
                "type": "Feature",
                "id": o.id,
                "geometry": {
                    "type": "Point",
                    "coordinates": [o.longitude, o.latitude],
                },
                "properties": {
                    "id": o.id,
                    "location_name": o.location_name,
                    "water_depth_cm": o.water_depth_cm,
                    "observation_source": o.observation_source,
                    "confidence": o.confidence,
                },
            })
        return {
            "type": "FeatureCollection",
            "name": "Mumbai Historical Flood Observations",
            "features": features,
        }

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown layer '{layer}'. Available: susceptibility, roads, reports, observations",
        )


@router.get("/road-segments", response_model=List[RoadSegmentResponse], tags=["Map"])
def list_road_segments(db: Session = Depends(get_db)):
    """List road corridors and subways."""
    return db.query(RoadSegment).all()
