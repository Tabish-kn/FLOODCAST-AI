# Project Memory: FloodCast AI

## 1. Project Vision & Identity

- **Product:** FloodCast AI — Hyperlocal Urban Flood-Risk Intelligence Platform.
- **Initial Study Area:** Mumbai Metropolitan Region (MMR), India (Bounds: Longitude 72.75°–73.05° E, Latitude 18.85°–19.30° N).
- **Core Philosophy:** Trustworthy decision support over false precision.
  - Distinguishes **Static Flood Susceptibility**, **Historical Flood Events**, **Remotely Detected Inundation**, and **Short-Horizon Forecasting**.
  - Communicates uncertainty, physical limitations, and data freshness explicitly.
  - Transparent participatory reporting with moderation verification.

---

## 2. Implementation Status: Complete & Verified MVP

- **Milestone Reached:** M7 (Open-Source GitHub Repository Suite Complete).
- **Artifacts Delivered:**
  - Complete Documentation Suite: [PRD.md](file:///a:/Sem%202/files/FLOODCAST%20AI/PRD.md), [ARCHITECTURE.md](file:///a:/Sem%202/files/FLOODCAST%20AI/ARCHITECTURE.md), [DESIGN.md](file:///a:/Sem%202/files/FLOODCAST%20AI/DESIGN.md), [RULES.md](file:///a:/Sem%202/files/FLOODCAST%20AI/RULES.md), [MEMORY.md](file:///a:/Sem%202/files/FLOODCAST%20AI/MEMORY.md), [TRACKER.md](file:///a:/Sem%202/files/FLOODCAST%20AI/TRACKER.md), and [README.md](file:///a:/Sem%202/files/FLOODCAST%20AI/README.md).
  - Open-Source Governance: [LICENSE](file:///a:/Sem%202/files/FLOODCAST%20AI/LICENSE) (Apache 2.0 with data disclaimer), [CONTRIBUTING.md](file:///a:/Sem%202/files/FLOODCAST%20AI/CONTRIBUTING.md), [CODE_OF_CONDUCT.md](file:///a:/Sem%202/files/FLOODCAST%20AI/CODE_OF_CONDUCT.md), [SECURITY.md](file:///a:/Sem%202/files/FLOODCAST%20AI/SECURITY.md), [CITATION.cff](file:///a:/Sem%202/files/FLOODCAST%20AI/CITATION.cff), [CHANGELOG.md](file:///a:/Sem%202/files/FLOODCAST%20AI/CHANGELOG.md), and [.editorconfig](file:///a:/Sem%202/files/FLOODCAST%20AI/.editorconfig).
  - GitHub Workflows & Templates: Automated CI workflow (`.github/workflows/ci.yml`), PR template (`.github/PULL_REQUEST_TEMPLATE.md`), and issue templates (`.github/ISSUE_TEMPLATE/{bug_report,feature_request,data_issue,config}.yml`).
  - Visual Documentation: Verified real dashboard preview screenshots placed in `docs/images/` and linked directly in the root `README.md`.
  - Backend: FastAPI service (`backend/app/main.py`) with complete REST API under `/api/v1/`, OpenAPI docs at `/docs`.
  - Persistence: SQLite spatial abstraction for zero-dependency local dev, with Docker PostgreSQL/PostGIS support for production.
  - ML Pipeline: `ml/dataset_generator.py`, `ml/train_susceptibility.py`, `ml/inference.py`, `ml/grid_generator.py`.
  - Calibrated Model: `data/models/baseline_rf_susceptibility.joblib` (Isotonic Regression calibrated Random Forest).
  - Validation Splits: Spatial Holdout on Island City (PR-AUC: 0.7182, Brier: 0.1649), Event Holdout on 2023 Deluge (PR-AUC: 0.7799, Brier: 0.1150).
  - Tests: 14 passing automated unit and integration tests (`pytest tests/ -v`).
  - Frontend: React 18 + Vite + TypeScript + MapLibre GL JS + Modern HSL Dark-Mode Design System. Production build verified with zero errors (`npm run build`).
  - Visual Verification: Executed full browser session testing all routes, map clicks, reporting flow, moderation actions, and model validation cards.

---

## 3. Selected Technologies & Conventions

- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Pytest, Uvicorn.
- **Frontend:** React 18, TypeScript, Vite, MapLibre GL JS, Lucide React, Modern CSS System.
- **Machine Learning:** Scikit-learn, NumPy, Pandas, Joblib (Isotonic Probability Calibration).
- **Spatial CRS:** WGS 84 (`EPSG:4326`) for API/GeoJSON interchange; UTM Zone 43N (`EPSG:32643`) for metric calculations.
- **API Convention:** Base path `/api/v1/`, OpenAPI documentation served automatically at `/docs`.

---

## 4. Non-Reversible Architectural Decisions

1. **Never combine Static Susceptibility and Live Forecast into an ambiguous single score.** Susceptibility reflects terrain and drainage geometry; forecasts require verified time-aligned precipitation nowcasts.
2. **Never claim live real-time radar or external sensor data when in offline/demo mode.** Displays `"ACTIVE MODE: Synthetic Demonstration Telemetry"`.
3. **Never expose reporter PII or precise residential locations on public endpoints.** Citizen reports are fuzzed by ~50m in residential areas, and submitter IP hashes are restricted to admin moderation tables.
4. **Zero-dependency local execution.** Works seamlessly with Python and Node without mandatory host Docker or cloud credentials.

---

## 5. Important Paths & Commands

- **Backend:** `backend/`
  - Run dev server: `uvicorn app.main:app --port 8000 --reload` (or `python -m uvicorn app.main:app --port 8000`)
  - Run tests: `pytest tests/ -v`
- **Frontend:** `frontend/`
  - Run dev server: `npm run dev`
  - Build bundle: `npm run build`
- **ML scripts:**
  - `python -m ml.dataset_generator`
  - `python -m ml.train_susceptibility`
  - `python -m ml.grid_generator`
