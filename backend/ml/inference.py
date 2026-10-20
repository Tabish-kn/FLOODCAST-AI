"""Inference service for FloodCast AI."""

import os
import joblib
import pandas as pd
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
from ml.features import compute_hydrological_features, haversine_distance_m, HISTORIC_DEPRESSIONS

REPO_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = REPO_ROOT / "data" / "models" / "baseline_rf_susceptibility.joblib"
_model = None


def get_model():
    global _model
    if _model is None:
        if MODEL_PATH.exists():
            _model = joblib.load(MODEL_PATH)
        else:
            raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}")
    return _model


def predict_location_risk(
    lat: float,
    lon: float,
    target_type: str = "SUSCEPTIBILITY",
    horizon_hours: int = 1,
    demo_mode: bool = True,
) -> Dict[str, Any]:
    """
    Executes model inference for a requested geographic location.
    Returns calibrated risk probability, risk tier, features, and honest uncertainty metadata.
    """
    features = compute_hydrological_features(lat, lon)

    # Check closest vulnerable subway / hotspot
    closest_subway = None
    min_dist_to_subway = float("inf")
    for dep in HISTORIC_DEPRESSIONS:
        d = haversine_distance_m(lat, lon, dep["lat"], dep["lon"])
        if d < min_dist_to_subway:
            min_dist_to_subway = d
            if d < 600:
                closest_subway = f"{dep['name']} (~{int(d)}m away)"

    model = get_model()
    feature_df = pd.DataFrame([features])

    # Calibrated probability from Isotonic model
    raw_probs = model.predict_proba(feature_df)[0]
    prob = float(raw_probs[1]) if len(raw_probs) > 1 else float(raw_probs[0])

    # Assign risk tier
    if prob < 0.25:
        tier = "LOW"
    elif prob < 0.55:
        tier = "MODERATE"
    elif prob < 0.78:
        tier = "HIGH"
    else:
        tier = "CRITICAL"

    # Uncertainty & Confidence calculation
    if min_dist_to_subway < 500:
        confidence = "HIGH"
    elif features["elevation_m"] > 25.0:
        confidence = "HIGH"
    else:
        confidence = "MODERATE"

    limitations = (
        "Model estimates terrain susceptibility from DEM, slope, and coastal choke points. "
        "Real-time municipal storm curb inlet debris and pump station operational status are unobserved."
    )

    now = datetime.utcnow()

    return {
        "prediction_id": f"pred-{int(now.timestamp())}-{abs(hash((lat, lon))) % 10000:04d}",
        "target_type": target_type,
        "latitude": lat,
        "longitude": lon,
        "risk_score": round(prob, 3),
        "risk_tier": tier,
        "issue_time": now,
        "target_window": f"{horizon_hours}h susceptibility baseline",
        "model_version": "v1.0-rf-mumbai",
        "features": features,
        "supporting_observations_count": 1 if min_dist_to_subway < 600 else 0,
        "nearby_subway_status": closest_subway,
        "uncertainty": {
            "confidence_tier": confidence,
            "is_calibrated": True,
            "data_freshness": "DEMO_MODE" if demo_mode else "LIVE",
            "missing_proxies": [
                "Municipal storm pump active status",
                "Sub-surface stormwater conduit sediment siltation level",
            ],
            "limitations_note": limitations,
        },
        "demo_mode": demo_mode,
    }
