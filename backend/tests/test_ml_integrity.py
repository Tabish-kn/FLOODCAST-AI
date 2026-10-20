import json
from pathlib import Path
import pytest
from ml.inference import get_model, predict_location_risk


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_model_artifact_exists_and_loads():
    model = get_model()
    assert model is not None
    # Check that it's a calibrated classifier
    assert hasattr(model, "predict_proba")


def test_evaluation_metrics_validity():
    metrics_path = REPO_ROOT / "data" / "models" / "evaluation_metrics.json"
    assert metrics_path.exists()
    with open(metrics_path, "r") as f:
        data = json.load(f)


    # Check spatial holdout exists and meets scientific requirements
    assert "spatial_holdout" in data
    assert data["spatial_holdout"]["pr_auc"] > 0.50
    assert 0.0 <= data["spatial_holdout"]["brier_score"] <= 0.35

    # Check event holdout exists
    assert "event_holdout" in data
    assert data["event_holdout"]["pr_auc"] > 0.50
    assert data["event_holdout"]["precision"] > 0.70


def test_no_fake_probabilities():
    # Model should output probabilities between 0 and 1
    pred = predict_location_risk(19.0888, 72.8427)  # Milan Subway
    assert 0.0 <= pred["risk_score"] <= 1.0
    assert pred["risk_tier"] in ["LOW", "MODERATE", "HIGH", "CRITICAL"]
    assert "features" in pred
    assert pred["features"]["elevation_m"] > 0
