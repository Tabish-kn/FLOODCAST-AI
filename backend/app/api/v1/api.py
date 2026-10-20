"""API v1 router registry."""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    map as map_endpoints,
    predictions,
    reports,
    events,
    models,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["System"])
api_router.include_router(map_endpoints.router, prefix="/map", tags=["Map"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(events.router, tags=["Historical"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
