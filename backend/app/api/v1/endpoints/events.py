"""Historical flood events and observations endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import FloodEvent, FloodObservation
from app.schemas.schemas import FloodEventResponse, FloodObservationResponse

router = APIRouter()


@router.get("/flood-events", response_model=List[FloodEventResponse], tags=["Historical"])
def list_flood_events(db: Session = Depends(get_db)):
    """List historical flood events with associated observations."""
    return db.query(FloodEvent).order_by(FloodEvent.event_date.desc()).all()


@router.get("/flood-observations", response_model=List[FloodObservationResponse], tags=["Historical"])
def list_flood_observations(db: Session = Depends(get_db)):
    """List documented flood observations across historical events."""
    return db.query(FloodObservation).all()
