"""Model status and scientific evaluation endpoints."""

import os
import json
from typing import List
from pathlib import Path
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import ModelVersion
from app.schemas.schemas import ModelVersionResponse

router = APIRouter()

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
METRICS_JSON_PATH = REPO_ROOT / "data" / "models" / "evaluation_metrics.json"



@router.get("/status", response_model=List[ModelVersionResponse], tags=["Models"])
def get_model_status(db: Session = Depends(get_db)):
    """Returns active models and associated evaluation splits."""
    return db.query(ModelVersion).all()


@router.get("/metrics", tags=["Models"])
def get_model_evaluation_metrics():
    """Returns detailed evaluation report including spatial and event holdout metrics."""
    if os.path.exists(METRICS_JSON_PATH):
        with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "status": "pending_evaluation",
        "message": "Evaluation metrics file not found. Run 'python -m ml.train_susceptibility' to generate.",
    }
