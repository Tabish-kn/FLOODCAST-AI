# Contributing to FloodCast AI

Thank you for your interest in contributing to **FloodCast AI**! We welcome researchers, ML engineers, geospatial data scientists, full-stack developers, and climate-resilience advocates.

To maintain scientific integrity, code quality, and ethical data handling, all contributors are requested to follow these guidelines.

---

## Code of Conduct

All contributors and participants agree to abide by our [Code of Conduct](file:///CODE_OF_CONDUCT.md). Please read it before participating.

---

## Development Setup

### 1. Prerequisites

- **Python**: 3.10, 3.11, or 3.12
- **Node.js**: v18.0.0 or higher (v20 LTS recommended)
- **Git**: 2.30+
- **Docker & Docker Compose** *(optional, for PostgreSQL/PostGIS testing)*

### 2. Clone the Repository

```bash
git clone https://github.com/[CONFIGURE_ORG_OR_USER]/floodcast-ai.git
cd floodcast-ai
```

### 3. Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt

# Copy environment configuration
cp .env.example .env

# Run database setup & migrations (uses SQLite by default for zero-config dev)
cd backend
python -c "from app.db.session import init_db; init_db()"

# Launch the FastAPI dev server
python -m uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000` with interactive Swagger docs at `http://127.0.0.1:8000/docs`.

### 4. Frontend Setup

In a new terminal window:

```bash
cd frontend
npm install
npm run dev
```

The frontend dashboard will run at `http://127.0.0.1:5173`.

---

## Branching & Commit Conventions

### Branch Naming

Use descriptive branch names with appropriate prefixes:

- `feat/susceptibility-calibration` — New feature or algorithm
- `fix/report-coordinate-snapping` — Bug fix
- `ml/xgboost-benchmark` — ML model experiments or pipelines
- `data/chirps-ingestion` — Data acquisition or preprocessing
- `docs/api-specification` — Documentation improvements
- `refactor/spatial-index` — Code refactoring without behavior change

### Commit Messages

We adhere to the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```text
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

Examples:

- `feat(ml): add isotonic calibration to random forest susceptibility model`
- `fix(backend): correct type validation in config CORS origin parser`
- `docs(readme): add interactive preview screenshots and architecture diagram`
- `test(api): add integration tests for citizen report verification endpoint`

---

## Code Style & Quality Standards

- **Python**:
  - Follow PEP 8 guidelines.
  - Type annotations are required on all new functions and class methods.
  - Format using `black` and lint with `flake8` or `ruff`.
- **TypeScript / React**:
  - Strict TypeScript mode (`strict: true` in `tsconfig.json`).
  - Use modular CSS / design system tokens; avoid arbitrary inline styling.
  - Verify zero lint/type errors: `npm run build`.
- **Markdown**:
  - Keep blank lines around headings, lists, tables, and fenced code blocks.
  - Always specify language identifiers on code fences (e.g., ````python````, ````bash````, ````mermaid````).

---

## Testing Expectations

No pull request will be merged without passing tests:

```bash
# Run backend test suite (14+ tests)
cd backend
pytest tests/ -v

# Run frontend build verification
cd ../frontend
npm run build
```

When introducing new API endpoints or ML modules:

- Write unit tests under `backend/tests/` matching the module name (e.g., `test_reports.py`).
- Use SQLite in-memory or fixture databases for fast, deterministic unit test execution.

---

## Machine Learning & Geospatial Standards

### 1. Scientific Reproducibility

- **Fix Random Seeds**: Always set explicit random seeds (e.g., `random_state=42`) in dataset generators and model initializations.
- **Leakage Prevention**: Never evaluate models on random uniform splits. Models must be evaluated on **Spatial Holdouts** (e.g., Island City held out from Suburbs) and **Temporal/Event Holdouts** (e.g., specific monsoon deluges held out from training).
- **Metric Integrity**: Report PR-AUC and Brier score alongside ROC-AUC or accuracy. In extreme flood prediction, positive class imbalance means ROC-AUC alone is misleading.

### 2. Geospatial Coordinates & Projections

- Internal storage and API payloads must use **WGS 84 (EPSG:4326)** coordinates formatted as `[longitude, latitude]`.
- Distance and buffer calculations must project to an appropriate UTM projection (e.g., **UTM Zone 43N / EPSG:32643** for Mumbai) before calculating Euclidean metrics.

### 3. Dataset Contributions

If contributing new environmental layers or observational records:

- **Provenance**: Document original data source, provider, and collection date.
- **License**: Verify that the license allows redistribution or derivative modeling. Do not commit proprietary data.
- **Spatial Resolution**: Document native resolution (e.g., 30m Copernicus DEM, 0.05° CHIRPS).

---

## Privacy & Safety

- **Spatial Fuzzing**: Community reports must not expose private residential addresses. Coordinates should be snapped to grid centroids or road intersections.
- **EXIF Stripping**: Never commit or publish images containing GPS metadata or identifying features of individuals.
- **Physical Safety**: We strictly discourage contributors from entering active floodwaters or hazards to collect observational data.

---

## Pull Request Checklist

Before submitting your PR, verify:

- [ ] Branch is branched from `master` (or latest `main`) and up to date.
- [ ] Backend tests pass: `pytest tests/ -v`.
- [ ] Frontend builds without TypeScript or bundling errors: `npm run build`.
- [ ] New functionality is covered by automated unit/integration tests.
- [ ] Relevant documentation (`README.md`, `ARCHITECTURE.md`, `PRD.md`) is updated.
- [ ] No secrets, `.env` files, or large raw dataset files are committed.
- [ ] Pull request description clearly explains the **motivation**, **implementation**, and **testing results**.
