"""Training and evaluation pipeline for Mumbai Flood Susceptibility Baseline."""

import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import (
    precision_score,
    recall_score,
    precision_recall_curve,
    auc,
    brier_score_loss,
)

FEATURE_COLS = [
    "elevation_m",
    "slope_degrees",
    "distance_to_waterway_m",
    "distance_to_storm_outfall_m",
    "impervious_surface_fraction",
    "historical_waterlogging_frequency",
    "is_depression",
]


def evaluate_split(y_true: np.ndarray, y_prob: np.ndarray) -> dict:
    """Compute rigorous classification and probability calibration metrics."""
    y_pred = (y_prob >= 0.5).astype(int)

    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))

    prec_curve, rec_curve, _ = precision_recall_curve(y_true, y_prob)
    pr_auc = float(auc(rec_curve, prec_curve))

    brier = float(brier_score_loss(y_true, y_prob))

    # Calibration curve (5 bins)
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=5, strategy="uniform")
    calibration_detail = {
        "prob_true": [float(x) for x in prob_true],
        "prob_pred": [float(x) for x in prob_pred],
    }

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "pr_auc": round(pr_auc, 4),
        "brier_score": round(brier, 4),
        "calibration_detail": calibration_detail,
        "sample_size": len(y_true),
        "positive_ratio": round(float(np.mean(y_true)), 4),
    }


def run_training_and_evaluation(
    dataset_path: str = "data/processed/mumbai_flood_benchmark.csv",
    output_dir: str = "data/models",
):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(dataset_path)

    print(f"Loaded dataset: {len(df)} samples.")

    # 1. Spatial Holdout Experiment
    # Train on Suburbs, test on Island City (South Mumbai)
    train_spatial = df[df["ward_region"].isin(["Western Suburbs", "Eastern Suburbs"])]
    test_spatial = df[df["ward_region"] == "Island City"]

    X_train_sp = train_spatial[FEATURE_COLS]
    y_train_sp = train_spatial["is_flooded"]
    X_test_sp = test_spatial[FEATURE_COLS]
    y_test_sp = test_spatial["is_flooded"]

    base_rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    calibrated_sp = CalibratedClassifierCV(estimator=base_rf, method="isotonic", cv=3)
    calibrated_sp.fit(X_train_sp, y_train_sp)

    probs_spatial = calibrated_sp.predict_proba(X_test_sp)[:, 1]
    metrics_spatial = evaluate_split(y_test_sp.values, probs_spatial)
    print(f"\n[SPATIAL HOLDOUT] Test Ward: Island City (N={len(y_test_sp)})")
    print(f"  PR-AUC: {metrics_spatial['pr_auc']:.4f}")
    print(f"  Brier Score: {metrics_spatial['brier_score']:.4f}")
    print(f"  Precision: {metrics_spatial['precision']:.4f}, Recall: {metrics_spatial['recall']:.4f}")

    # 2. Event / Temporal Holdout Experiment
    # Train on events <= 2021, test on 2023 deluge
    train_event = df[df["event_year"] <= 2021]
    test_event = df[df["event_year"] == 2023]

    X_train_ev = train_event[FEATURE_COLS]
    y_train_ev = train_event["is_flooded"]
    X_test_ev = test_event[FEATURE_COLS]
    y_test_ev = test_event["is_flooded"]

    base_rf_ev = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    calibrated_ev = CalibratedClassifierCV(estimator=base_rf_ev, method="isotonic", cv=3)
    calibrated_ev.fit(X_train_ev, y_train_ev)

    probs_event = calibrated_ev.predict_proba(X_test_ev)[:, 1]
    metrics_event = evaluate_split(y_test_ev.values, probs_event)
    print(f"\n[EVENT HOLDOUT] Test Year: 2023 Deluge (N={len(y_test_ev)})")
    print(f"  PR-AUC: {metrics_event['pr_auc']:.4f}")
    print(f"  Brier Score: {metrics_event['brier_score']:.4f}")
    print(f"  Precision: {metrics_event['precision']:.4f}, Recall: {metrics_event['recall']:.4f}")

    # 3. Final Production Model
    # Trained on all verified Mumbai benchmark samples with 5-fold calibration
    final_rf = RandomForestClassifier(n_estimators=150, max_depth=7, random_state=42)
    final_calibrated = CalibratedClassifierCV(estimator=final_rf, method="isotonic", cv=5)
    final_calibrated.fit(df[FEATURE_COLS], df["is_flooded"])

    # Feature importances from base estimator
    final_rf.fit(df[FEATURE_COLS], df["is_flooded"])
    importances = {col: round(float(imp), 4) for col, imp in zip(FEATURE_COLS, final_rf.feature_importances_)}

    # Save artifacts
    model_artifact_path = Path(output_dir) / "baseline_rf_susceptibility.joblib"
    joblib.dump(final_calibrated, model_artifact_path)
    print(f"\nSaved calibrated model to: {model_artifact_path}")

    evaluation_report = {
        "model_version": "v1.0-rf-mumbai",
        "target_type": "SUSCEPTIBILITY",
        "feature_importances": importances,
        "spatial_holdout": metrics_spatial,
        "event_holdout": metrics_event,
        "training_samples_total": len(df),
    }

    metrics_json_path = Path(output_dir) / "evaluation_metrics.json"
    with open(metrics_json_path, "w") as f:
        json.dump(evaluation_report, f, indent=2)
    print(f"Saved evaluation metrics to: {metrics_json_path}")


if __name__ == "__main__":
    run_training_and_evaluation()
