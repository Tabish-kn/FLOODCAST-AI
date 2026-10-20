# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Satellite inundation segmentation pipeline leveraging Sentinel-1 SAR imagery.
- Road-segment network exposure weighting via OpenStreetMap graph ingestion.
- Short-horizon precipitation forecasting with calibrated ensemble feeds.

## [1.0.0] - 2026-10-21

### Added

- **Geospatial Feature Engineering Pipeline**:
  - Topographic and environmental feature extraction (`elevation_m`, `slope_deg`, `twi`, `distance_to_drain_m`, `distance_to_coast_m`, `impervious_surface_pct`, `land_cover_code`).
  - Synthetic yet spatially grounded Mumbai benchmark dataset generator (`ml/dataset_generator.py`) with 5,000 spatial observations.
- **Machine Learning Susceptibility Baseline**:
  - Calibrated Random Forest model (`ml/train_susceptibility.py`) combining tree ensembles with Isotonic probability calibration.
  - Rigorous scientific validation framework: Spatial Holdout (Island City) and Event Holdout (2023 Deluge) splits preventing spatial/temporal leakage.
  - Susceptibility grid generator (`ml/grid_generator.py`) compiling 1,200+ hex/polygon centroids across Greater Mumbai into optimized GeoJSON.
- **FastAPI REST Backend**:
  - Asynchronous FastAPI service supporting both SQLite (zero-config local dev) and PostgreSQL 16 + PostGIS (production container).
  - Health check endpoint (`/api/v1/health`) with database connectivity verification.
  - Susceptibility endpoints (`/api/v1/susceptibility/grid`, `/api/v1/susceptibility/predict`).
  - Community flood reporting endpoints (`POST /api/v1/reports`, `GET /api/v1/reports`, `PATCH /api/v1/reports/{id}/verify`).
  - Historical deluges catalog (`/api/v1/deluges`).
  - Scientific validation metrics endpoint (`/api/v1/validation/metrics`).
  - Full suite of 14 unit and integration tests passing (`pytest tests/ -v`).
- **Modern Interactive Frontend Dashboard**:
  - React 18 + TypeScript + Vite responsive web application.
  - MapLibre GL JS integration displaying interactive susceptibility layers and community waterlogging points.
  - Real-time Point Risk Inspector querying machine learning inference on click.
  - Historical deluge timeline inspector and citizen reporting modal with client-side coordinate snapping.
  - Moderation queue dashboard for verifying or rejecting community reports.
  - Scientific Model Validation transparency panel rendering PR-AUC, Brier score, and calibration curves.
  - Clean HSL color system, dark mode aesthetic, and glassmorphic micro-interactions.
- **DevOps & Open Source Ecosystem**:
  - `docker-compose.yml` for multi-container deployment with PostGIS.
  - GitHub Actions CI workflow for Python tests and frontend build validation.
  - Comprehensive open-source governance (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE`, `CITATION.cff`, `.editorconfig`).
  - GitHub issue templates for bug reports, feature requests, and geospatial data issues.
