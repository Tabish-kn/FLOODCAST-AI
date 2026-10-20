# FloodCast AI: Hyperlocal Flood-Risk Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178c6.svg)](https://www.typescriptlang.org)
[![MapLibre](https://img.shields.io/badge/MapLibre-GL%20JS-blueviolet.svg)](https://maplibre.org)
![Tests](https://img.shields.io/badge/Tests-14%20Passed-brightgreen.svg)

FloodCast AI is an extensible, research-oriented, and startup-ready climate-tech platform designed to provide hyperlocal urban flood-risk intelligence, initially focused on the **Mumbai Metropolitan Region (MMR)**, Maharashtra, India.

---

## 1. Core Principles & Scientific Integrity

1. **Four Distinct Capabilities:**
   - **Static Flood Susceptibility:** Permanent topographic depression, slope, and drainage baseline risk.
   - **Historical Flood Observations:** Documented ground-truth flood footprints from major Mumbai monsoons (July 2005, August 2017, July 2021, July 2023).
   - **Participatory Reporting:** Community and fleet driver ground observations with transparent moderation status.
   - **Short-Horizon Forecasting:** 1–6 hour predictive hazard conditioned on incoming radar nowcasts and antecedent soil moisture.
2. **Never Color Alone:** Risk is always triple-encoded: Color (Emerald/Amber/Orange/Rose-Red) + Text Label (LOW/MODERATE/HIGH/CRITICAL) + Distinct Icon.
3. **Calibrated Probabilities:** Machine learning predictions use Isotonic Regression probability calibration evaluated on spatial and event holdouts rather than uncalibrated raw classifier outputs.
4. **Zero Phantom Claims:** Transparent state indicators explicitly label synthetic fixtures when running in offline or demonstration mode.

---

## 2. Study Area: Mumbai Metropolitan Region (MMR)

- **Geographic Bounding Box:**
  - Latitude: `18.85° N` to `19.30° N`
  - Longitude: `72.75° E` to `73.05° E`
- **Coordinate Reference Systems:**
  - Storage & API Interchange: WGS 84 (`EPSG:4326`)
  - Metric Distance & Slope Calculations: UTM Zone 43N (`EPSG:32643`)
- **Critical Subways & Corridors Tracked:**
  - Milan Subway (Santacruz)
  - Andheri Subway (SV Road)
  - Malad Subway
  - Hindmata Junction / Parel
  - Gandhi Market / King's Circle
  - Kurla West / Mithi River corridor

---

## 3. Architecture Overview

```text
floodcast-ai/
├── PRD.md                       # Product Requirements Document
├── ARCHITECTURE.md              # Technical Architecture & ADRs
├── DESIGN.md                    # UI/UX Design System Specification
├── RULES.md                     # Engineering & Scientific Rulebook
├── TRACKER.md                   # Development Task Tracker
├── MEMORY.md                    # Persistent Project Memory
├── docker-compose.yml           # Production multi-container orchestration
│
├── backend/                     # Python 3.12 + FastAPI Backend
│   ├── app/
│   │   ├── api/v1/endpoints/    # Health, Map, Predictions, Reports, Events, Models
│   │   ├── core/                # Config, Security, Exceptions
│   │   ├── db/                  # Session, Base, Seed Data
│   │   ├── models/              # SQLAlchemy 2.0 ORM Entities
│   │   └── schemas/             # Pydantic v2 Schemas
│   ├── tests/                   # Pytest test suite (14 passing tests)
│   └── pyproject.toml
│
├── frontend/                    # React 18 + TypeScript + Vite + MapLibre GL JS
│   ├── src/
│   │   ├── components/          # InteractiveMap, RiskInspectorPanel, ReportModal, etc.
│   │   ├── services/            # Typed API Client
│   │   ├── types/               # TypeScript Contracts
│   │   └── index.css            # Modern HSL Dark-Mode Design System
│   └── package.json
│
├── ml/                          # Machine Learning & Hydrological Pipeline
│   ├── features.py              # Topographic & hydrological feature engineering
│   ├── dataset_generator.py     # Mumbai benchmark training & validation generator
│   ├── train_susceptibility.py  # Model training with spatial and event holdout splits
│   ├── inference.py             # Live inference with uncertainty quantification
│   └── grid_generator.py        # Susceptibility GeoJSON grid generator
│
└── data/                        # Datasets, models, and GeoJSON fixtures
    ├── models/                  # Calibrated model artifacts & evaluation metrics
    └── fixtures/                # Mumbai susceptibility grid GeoJSON
```

---

## 4. Quick Start (Local Development)

### Prerequisites

- Python 3.12+
- Node.js v18+ and npm

### 1. Start the Backend API

```bash
# From repository root
cd backend

# Install dependencies (or pip install -r requirements)
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings shapely scikit-learn pandas numpy joblib httpx pytest

# Seed database and start development server
python -m uvicorn app.main:app --port 8000 --reload
```

The FastAPI backend will start at `http://localhost:8000`.

- OpenAPI Docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 2. Start the Frontend Web Application

```bash
# In a new terminal, from repository root
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 5. Machine Learning Pipeline Execution

To reproduce the benchmark dataset, train the baseline model, and evaluate on spatial holdouts:

```bash
# 1. Generate the Mumbai benchmark dataset
python -m ml.dataset_generator

# 2. Train and evaluate the Calibrated Random Forest model
python -m ml.train_susceptibility

# 3. Generate the canonical MapLibre GeoJSON susceptibility grid
python -m ml.grid_generator
```

### Verified Scientific Validation Results

- **Spatial Holdout (Tested on Island City / South Mumbai):**
  - PR-AUC: `0.7182`
  - Brier Score: `0.1649`
  - Precision: `87.64%`
- **Event Holdout (Tested on July 2023 Monsoon Deluge):**
  - PR-AUC: `0.7799`
  - Brier Score: `0.1150`
  - Precision: `93.55%`

---

## 6. Running Tests

Run the complete automated backend and ML test suite:

```bash
cd backend
pytest tests/ -v
```

All 14 unit and integration tests verify:

- Geographic coordinate boundary enforcement
- Hydrological feature extraction
- Low-lying depression identification (Hindmata, Milan Subway)
- Elevated control points (Malabar Hill, Powai)
- Location risk inspection API
- Community report submission, fuzzing, and moderator review
- Calibration and absence of fabricated probabilities

---

## 7. Production Deployment (Docker Compose)

For production deployments with PostgreSQL 16 + PostGIS:

```bash
docker-compose up --build
```

This spins up:

- `db`: PostGIS database with spatial indexing
- `backend`: FastAPI container with multi-worker Uvicorn
- `frontend`: High-performance Nginx container serving static production bundle
