"""Structured domain exceptions for FloodCast AI."""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class FloodCastException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str,
        extra: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": detail,
                "extra": extra or {},
            },
        )


class LocationOutOfBoundsException(FloodCastException):
    def __init__(self, lat: float, lon: float):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requested coordinates ({lat}, {lon}) are outside the active Mumbai study area bounds.",
            error_code="LOCATION_OUT_OF_BOUNDS",
            extra={"latitude": lat, "longitude": lon},
        )


class ModelNotAvailableException(FloodCastException):
    def __init__(self, target: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Prediction model for target '{target}' is currently unavailable or uncalibrated.",
            error_code="MODEL_NOT_AVAILABLE",
            extra={"target": target},
        )


class ResourceNotFoundException(FloodCastException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id '{identifier}' was not found.",
            error_code="RESOURCE_NOT_FOUND",
            extra={"resource": resource, "id": identifier},
        )
