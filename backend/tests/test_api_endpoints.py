"""Integration tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_and_readiness():
    resp_health = client.get("/health")
    assert resp_health.status_code == 200
    assert resp_health.json()["status"] == "healthy"

    resp_ready = client.get("/ready")
    assert resp_ready.status_code == 200
    assert resp_ready.json()["status"] == "ready"


def test_metadata():
    resp = client.get("/api/v1/metadata")
    assert resp.status_code == 200
    data = resp.json()
    assert data["study_area"]["name"] == "Mumbai Metropolitan Region"
    assert "crs" in data["study_area"]


def test_map_layers_and_roads():
    resp_layers = client.get("/api/v1/map/layers")
    assert resp_layers.status_code == 200
    assert len(resp_layers.json()["layers"]) >= 4

    resp_roads = client.get("/api/v1/map/features?layer=roads")
    assert resp_roads.status_code == 200
    data = resp_roads.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) >= 5


def test_location_risk_prediction_valid():
    # Hindmata coordinates (19.0069, 72.8415)
    resp = client.get("/api/v1/predictions/query?lat=19.0069&lon=72.8415")
    assert resp.status_code == 200
    data = resp.json()
    assert data["risk_tier"] in ["HIGH", "CRITICAL"]
    assert 0.0 <= data["risk_score"] <= 1.0
    assert "features" in data
    assert "uncertainty" in data
    assert data["uncertainty"]["is_calibrated"] is True


def test_location_risk_out_of_bounds():
    # London coordinates (51.5074, -0.1278) outside Mumbai
    resp = client.get("/api/v1/predictions/query?lat=51.5074&lon=-0.1278")
    assert resp.status_code == 400
    data = resp.json()
    assert data["error_code"] == "LOCATION_OUT_OF_BOUNDS"


def test_community_report_submission_and_review():
    # 1. Submit valid report
    new_report = {
        "latitude": 19.0720,
        "longitude": 72.8380,
        "category": "ROAD_IMPASSABLE",
        "depth_range": "1-2 ft",
        "road_passability": "IMPASSABLE",
        "consent_granted": True,
        "is_residential": False,
    }
    create_resp = client.post("/api/v1/reports", json=new_report)
    assert create_resp.status_code == 201
    report_data = create_resp.json()
    assert report_data["verification_status"] == "UNVERIFIED"
    report_id = report_data["id"]

    # 2. Moderate report (review)
    review_payload = {
        "decision": "VERIFIED",
        "reason": "Traffic control camera confirmed water accumulation.",
        "reviewer_id": "test-admin",
    }
    review_resp = client.post(f"/api/v1/reports/{report_id}/review", json=review_payload)
    assert review_resp.status_code == 200
    updated_report = review_resp.json()
    assert updated_report["verification_status"] == "VERIFIED"


def test_historical_flood_events():
    resp = client.get("/api/v1/flood-events")
    assert resp.status_code == 200
    events = resp.json()
    assert len(events) >= 4
    # July 2005 deluge
    assert any("2005" in e["name"] for e in events)
