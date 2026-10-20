"""Database initialization and seeding script."""

import json
from datetime import datetime
from app.db.session import engine, SessionLocal, Base
from app.models.entities import (
    StudyArea,
    RoadSegment,
    FloodEvent,
    FloodObservation,
    CommunityReport,
    ReportReview,
    ModelVersion,
    ModelEvaluation,
)
from app.core.config import settings


def seed_database():
    """Initializes schema and populates canonical Mumbai fixtures."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Study Area: Mumbai MMR
        study_area = db.query(StudyArea).filter(StudyArea.name == settings.STUDY_AREA_NAME).first()
        if not study_area:
            study_area = StudyArea(
                name=settings.STUDY_AREA_NAME,
                center_lat=settings.STUDY_AREA_CENTER_LAT,
                center_lon=settings.STUDY_AREA_CENTER_LON,
                min_lat=settings.STUDY_AREA_MIN_LAT,
                max_lat=settings.STUDY_AREA_MAX_LAT,
                min_lon=settings.STUDY_AREA_MIN_LON,
                max_lon=settings.STUDY_AREA_MAX_LON,
                boundary_geojson={
                    "type": "Polygon",
                    "coordinates": [[
                        [settings.STUDY_AREA_MIN_LON, settings.STUDY_AREA_MIN_LAT],
                        [settings.STUDY_AREA_MAX_LON, settings.STUDY_AREA_MIN_LAT],
                        [settings.STUDY_AREA_MAX_LON, settings.STUDY_AREA_MAX_LAT],
                        [settings.STUDY_AREA_MIN_LON, settings.STUDY_AREA_MAX_LAT],
                        [settings.STUDY_AREA_MIN_LON, settings.STUDY_AREA_MIN_LAT],
                    ]],
                },
            )
            db.add(study_area)
            db.commit()
            db.refresh(study_area)
            print(f"Created StudyArea: {study_area.name}")

        # 2. Road Segments & Underpasses
        existing_roads = db.query(RoadSegment).count()
        if existing_roads == 0:
            roads_data = [
                {
                    "name": "Milan Subway (Santacruz - Vile Parle)",
                    "highway_type": "underpass",
                    "is_subway": True,
                    "elevation_m": 2.1,
                    "historical_vulnerability": "CRITICAL",
                    "line": [[72.8410, 19.0880], [72.8435, 19.0895]],
                },
                {
                    "name": "Andheri Subway (SV Road Connection)",
                    "highway_type": "underpass",
                    "is_subway": True,
                    "elevation_m": 2.3,
                    "historical_vulnerability": "CRITICAL",
                    "line": [[72.8450, 19.1190], [72.8475, 19.1205]],
                },
                {
                    "name": "Malad Subway (Malad West - East)",
                    "highway_type": "underpass",
                    "is_subway": True,
                    "elevation_m": 2.4,
                    "historical_vulnerability": "CRITICAL",
                    "line": [[72.8470, 19.1860], [72.8495, 19.1870]],
                },
                {
                    "name": "Hindmata Flyover Underpass (Dr. Ambedkar Rd)",
                    "highway_type": "primary",
                    "is_subway": False,
                    "elevation_m": 3.1,
                    "historical_vulnerability": "HIGH",
                    "line": [[72.8405, 19.0050], [72.8425, 19.0090]],
                },
                {
                    "name": "Gandhi Market / King's Circle Stretch",
                    "highway_type": "primary",
                    "is_subway": False,
                    "elevation_m": 2.7,
                    "historical_vulnerability": "HIGH",
                    "line": [[72.8550, 19.0310], [72.8590, 19.0350]],
                },
                {
                    "name": "Western Express Highway (Bandra - Dahisar)",
                    "highway_type": "trunk",
                    "is_subway": False,
                    "elevation_m": 8.5,
                    "historical_vulnerability": "MODERATE",
                    "line": [[72.8520, 19.0600], [72.8560, 19.1500], [72.8620, 19.2400]],
                },
                {
                    "name": "Eastern Express Highway (Sion - Mulund)",
                    "highway_type": "trunk",
                    "is_subway": False,
                    "elevation_m": 7.2,
                    "historical_vulnerability": "MODERATE",
                    "line": [[72.8750, 19.0450], [72.9100, 19.1200], [72.9500, 19.1800]],
                },
                {
                    "name": "SV Road (Bandra to Borivali)",
                    "highway_type": "primary",
                    "is_subway": False,
                    "elevation_m": 5.4,
                    "historical_vulnerability": "HIGH",
                    "line": [[72.8390, 19.0550], [72.8440, 19.1300], [72.8550, 19.2200]],
                },
            ]

            for r in roads_data:
                seg = RoadSegment(
                    study_area_id=study_area.id,
                    name=r["name"],
                    highway_type=r["highway_type"],
                    is_subway=r["is_subway"],
                    elevation_m=r["elevation_m"],
                    historical_vulnerability=r["historical_vulnerability"],
                    line_geojson={"type": "LineString", "coordinates": r["line"]},
                )
                db.add(seg)
            db.commit()
            print(f"Added {len(roads_data)} RoadSegments.")

        # 3. Historical Flood Events & Observations
        if db.query(FloodEvent).count() == 0:
            events_data = [
                {
                    "name": "Mumbai Great Deluge 2005",
                    "date": "2005-07-26",
                    "total_rain": 944.0,
                    "peak_rain": 125.0,
                    "desc": "Highest single-day precipitation in Mumbai history; extreme high tide coincided with Mithi River overflow.",
                    "obs": [
                        {"name": "Kurla West / LBS Marg", "lat": 19.0680, "lon": 72.8790, "depth_cm": 150.0},
                        {"name": "Kalina / Air India Colony", "lat": 19.0740, "lon": 72.8630, "depth_cm": 180.0},
                        {"name": "Milan Subway", "lat": 19.0888, "lon": 72.8427, "depth_cm": 220.0},
                    ],
                },
                {
                    "name": "August 2017 Cloudburst Deluge",
                    "date": "2017-08-29",
                    "total_rain": 331.0,
                    "peak_rain": 85.0,
                    "desc": "Paralyzed Mumbai suburban train network; severe flooding at Hindmata and Gandhi Market.",
                    "obs": [
                        {"name": "Hindmata Junction", "lat": 19.0069, "lon": 72.8415, "depth_cm": 90.0},
                        {"name": "Gandhi Market King's Circle", "lat": 19.0330, "lon": 72.8570, "depth_cm": 85.0},
                        {"name": "Andheri Subway", "lat": 19.1197, "lon": 72.8464, "depth_cm": 140.0},
                    ],
                },
                {
                    "name": "July 2021 Chembur / Suburban Inundation",
                    "date": "2021-07-18",
                    "total_rain": 253.0,
                    "peak_rain": 72.0,
                    "desc": "Severe nocturnal cloudburst triggering localized urban landslides and severe waterlogging.",
                    "obs": [
                        {"name": "Chembur Shell Colony", "lat": 19.0550, "lon": 72.8980, "depth_cm": 75.0},
                        {"name": "Malad Subway", "lat": 19.1865, "lon": 72.8485, "depth_cm": 110.0},
                    ],
                },
                {
                    "name": "July 2023 Red Alert Downpour",
                    "date": "2023-07-26",
                    "total_rain": 287.0,
                    "peak_rain": 68.0,
                    "desc": "Prolonged monsoon downpour inundating subways and halting western line slow trains.",
                    "obs": [
                        {"name": "Milan Subway", "lat": 19.0888, "lon": 72.8427, "depth_cm": 130.0},
                        {"name": "Bandra East Kalanagar", "lat": 19.0595, "lon": 72.8525, "depth_cm": 60.0},
                    ],
                },
            ]

            for ev in events_data:
                fe = FloodEvent(
                    name=ev["name"],
                    event_date=ev["date"],
                    total_rainfall_mm=ev["total_rain"],
                    peak_intensity_mm_h=ev["peak_rain"],
                    description=ev["desc"],
                )
                db.add(fe)
                db.commit()
                db.refresh(fe)

                for ob in ev["obs"]:
                    fo = FloodObservation(
                        event_id=fe.id,
                        location_name=ob["name"],
                        latitude=ob["lat"],
                        longitude=ob["lon"],
                        water_depth_cm=ob["depth_cm"],
                        observation_source="MUNICIPAL_DISASTER_LOG",
                        confidence="HIGH",
                    )
                    db.add(fo)
            db.commit()
            print(f"Added {len(events_data)} FloodEvents and observations.")

        # 4. Community Reports (Sample verified and unverified reports)
        if db.query(CommunityReport).count() == 0:
            sample_reports = [
                {
                    "lat": 19.0072,
                    "lon": 72.8418,
                    "cat": "WATERLOGGING",
                    "depth": "1-2 ft",
                    "pass": "IMPASSABLE",
                    "status": "VERIFIED",
                    "notes": "Hindmata cinema junction water reaching knee level, traffic diverted to flyover.",
                },
                {
                    "lat": 19.0890,
                    "lon": 72.8425,
                    "cat": "ROAD_IMPASSABLE",
                    "depth": ">2 ft",
                    "pass": "IMPASSABLE",
                    "status": "VERIFIED",
                    "notes": "Milan subway completely shut by traffic police due to 3ft water.",
                },
                {
                    "lat": 19.0335,
                    "lon": 72.8575,
                    "cat": "DRAIN_OVERFLOW",
                    "depth": "6-12 in",
                    "pass": "TWO_WHEELERS_ONLY",
                    "status": "VERIFIED",
                    "notes": "Gandhi market storm drain backing up on north-bound carriageway.",
                },
                {
                    "lat": 19.0685,
                    "lon": 72.8795,
                    "cat": "WATERLOGGING",
                    "depth": "1-2 ft",
                    "pass": "HEAVY_ONLY",
                    "status": "UNVERIFIED",
                    "notes": "LBS Marg near Kurla station water accumulating rapidly.",
                },
                {
                    "lat": 19.1195,
                    "lon": 72.8460,
                    "cat": "ROAD_IMPASSABLE",
                    "depth": ">2 ft",
                    "pass": "IMPASSABLE",
                    "status": "UNVERIFIED",
                    "notes": "Andheri subway barrier down, car stuck in middle.",
                },
            ]

            for rep in sample_reports:
                cr = CommunityReport(
                    study_area_id=study_area.id,
                    latitude=rep["lat"],
                    longitude=rep["lon"],
                    fuzzed_latitude=rep["lat"],
                    fuzzed_longitude=rep["lon"],
                    category=rep["cat"],
                    depth_range=rep["depth"],
                    road_passability=rep["pass"],
                    verification_status=rep["status"],
                    consent_granted=True,
                    client_ip_hash="sha256-demo-seed-ip",
                    notes=rep["notes"],
                )
                db.add(cr)
                db.commit()
                db.refresh(cr)

                if rep["status"] == "VERIFIED":
                    review = ReportReview(
                        report_id=cr.id,
                        reviewer_id="chief-meteorology-reviewer",
                        decision="VERIFIED",
                        reason="Confirmed by traffic police waterlogging bulletin.",
                    )
                    db.add(review)
            db.commit()
            print(f"Added {len(sample_reports)} CommunityReports with verification records.")

        # 5. Model Version & Evaluation Records
        if db.query(ModelVersion).count() == 0:
            mv = ModelVersion(
                model_name="RandomForest Susceptibility Baseline",
                version_tag="v1.0-rf-mumbai",
                target_type="SUSCEPTIBILITY",
                parameters={
                    "n_estimators": 150,
                    "max_depth": 7,
                    "calibration": "isotonic",
                    "features": [
                        "elevation_m",
                        "slope_degrees",
                        "distance_to_waterway_m",
                        "distance_to_storm_outfall_m",
                        "impervious_surface_fraction",
                        "historical_waterlogging_frequency",
                        "is_depression",
                    ],
                },
                artifact_path="data/models/baseline_rf_susceptibility.joblib",
                is_active=True,
            )
            db.add(mv)
            db.commit()
            db.refresh(mv)

            # Add evaluation splits
            eval_sp = ModelEvaluation(
                model_version_id=mv.id,
                split_type="SPATIAL_HOLDOUT (Island City)",
                pr_auc=0.7182,
                brier_score=0.1649,
                precision_at_k=0.8764,
                recall_at_k=0.3786,
                metrics_detail={
                    "test_region": "Island City",
                    "train_region": "Western & Eastern Suburbs",
                },
            )
            eval_ev = ModelEvaluation(
                model_version_id=mv.id,
                split_type="EVENT_HOLDOUT (2023 Deluge)",
                pr_auc=0.7799,
                brier_score=0.1150,
                precision_at_k=0.9355,
                recall_at_k=0.5273,
                metrics_detail={"test_event": "2023 Monsoon Peak Deluge"},
            )
            db.add(eval_sp)
            db.add(eval_ev)
            db.commit()
            print("Added ModelVersion v1.0 and ModelEvaluations.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
