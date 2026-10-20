"""Configuration management for FloodCast AI."""

import json
from typing import Any, List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "FloodCast AI"
    APP_VERSION: str = "1.0.0"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            if v.startswith("["):
                loaded = json.loads(v)
                if isinstance(loaded, list):
                    return [str(item) for item in loaded]
                return [str(loaded)]
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return [str(item) for item in v]
        return []


    # Database Configuration (Default SQLite for zero-config local dev)
    DATABASE_URL: str = "sqlite:///./floodcast.db"

    # Security Settings
    SECRET_KEY: str = "dev-secret-key-change-in-production-must-be-32-chars-min"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Study Area: Mumbai MMR Bounding Box
    STUDY_AREA_NAME: str = "Mumbai Metropolitan Region"
    STUDY_AREA_MIN_LON: float = 72.75
    STUDY_AREA_MAX_LON: float = 73.05
    STUDY_AREA_MIN_LAT: float = 18.85
    STUDY_AREA_MAX_LAT: float = 19.30
    STUDY_AREA_CENTER_LAT: float = 19.0760
    STUDY_AREA_CENTER_LON: float = 72.8777

    # Operational & Demo Mode
    DEMO_MODE: bool = True
    OPEN_METEO_API_ENABLED: bool = True
    COPENICUS_DATA_SPACE_ENABLED: bool = False

    # Storage Paths
    DATA_DIR: str = "./data"
    MODEL_ARTIFACTS_DIR: str = "./data/models"
    UPLOAD_DIR: str = "./data/uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
