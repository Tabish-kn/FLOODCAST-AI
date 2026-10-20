# Product Requirements Document (PRD): FloodCast AI

## 1. Product Vision

FloodCast AI is an extensible, research-oriented, and startup-ready hyperlocal urban flood-risk intelligence platform initially focused on the Mumbai Metropolitan Region (MMR), India. It bridges geospatial data, machine learning, remote sensing, weather information, and community-reported ground observations to estimate localized urban flood vulnerability, waterlogging occurrence, and short-horizon risk exposure.

The platform is built on an unwavering principle: **Trustworthy decision support over false precision.** It explicitly distinguishes between:

1. **Static Flood Susceptibility** (topographic, hydrological, and land-use baseline vulnerability).
2. **Historical Flood Observations & Events** (past recorded waterlogging, municipal data, and verified community records).
3. **Remotely Detected Inundation** (SAR satellite-derived surface water detection such as Sentinel-1 change analysis).
4. **Short-Horizon Flood Forecasting** (predictive risk conditioned on rainfall nowcasts/forecasts and antecedent wetness).

A susceptibility score or historical flood footprint is **never** misrepresented as a live forecast.

---

## 2. Problem Statement

Mumbai experiences extreme precipitation events during the South-West Monsoon (June–September), coupled with high astronomical tides, reclaimed topography, and strained municipal storm drainage networks (e.g., Mithi River, storm outfalls).

Existing solutions suffer from several critical shortcomings:

- **Macro-scale weather warnings:** Severe weather alerts are issued for entire city districts (e.g., "Red Alert for Mumbai Suburban"), failing to identify which specific underpasses, intersections, or logistics corridors are impassable.
- **Opacities and Black-Box Claims:** Models present single probability scores without explaining antecedent soil wetness, drainage limitations, or source confidence.
- **Disconnect with Ground Truth:** Municipal authorities and citizens report localized waterlogging on social channels, but this rich participatory data is rarely ingested, verified, or used to improve predictive ML pipelines.
- **Emergency Claims Without Validation:** Apps mislead logistics planners and citizens by conflating static terrain depression maps with real-time water depth.

FloodCast AI provides an open, reproducible, uncertainty-aware decision-support platform designed to monitor, analyze, and forecast flood risks hyperlocally.

---

## 3. Target Users & Personas

### 3.1 Commercial Persona: Logistics & Dispatch Lead (Priority 1)

- **Name:** Rajesh Sharma (Fleet Operations Lead, Western Suburban Express)
- **Pain Points:** Delivery vans trapped in submerged underpasses (e.g., Milan Subway, Andheri Subway, Hindmata); cargo damage in ground-level storage hubs; delivery delays.
- **Needs:** Hyperlocal road passability warnings, 1–6 hour risk indicators ahead of high-intensity rain bands, clear freshness indicators for road segment data.

### 3.2 Facility & Property Manager

- **Name:** Priya Nair (Industrial Park Asset Manager, Kurla/Bhandup)
- **Pain Points:** Unplanned water ingress into basement electrical substations and ground inventory; high business interruption insurance claims.
- **Needs:** Site-specific susceptibility scoring, historical flood comparison, alert lead-time for activating sump pumps and flood barriers.

### 3.3 Climate-Risk Researcher & Geospatial Data Scientist

- **Name:** Dr. Amit Deshmukh (Urban Hydrology Researcher)
- **Pain Points:** Lack of open, benchmarked event datasets; opaque proprietary models; absence of proper spatial/temporal validation holdouts.
- **Needs:** Open spatial APIs, raw data provenance, reproducible feature pipelines (elevation, slope, imperviousness, rainfall), ML model evaluation metrics (PR-AUC, Brier score, calibration curves).

### 3.4 Community Contributor

- **Name:** Sana Merchant (Resident & Daily Commuter, Dadar/Parel)
- **Pain Points:** Commute disruptions, unsafe walking routes during torrential downpours; no easy way to notify others or verify flood depth safely.
- **Needs:** Frictionless mobile reporting of waterlogging, intuitive privacy controls, visual verification status of submitted reports.

### 3.5 Authorized Administrator & Data Reviewer

- **Name:** Municipal / Research Reviewer
- **Needs:** Moderation interface to verify, classify, or reject citizen reports; audit trail; duplicate report detection.

---

## 4. MVP Scope vs. Future Roadmap

### 4.1 In MVP Scope

- Core study area: Mumbai Metropolitan Region (focused bounding box covering Island City, Western Suburbs, and Eastern Suburbs).
- Map-centric interactive web application (MapLibre GL JS + React/TypeScript) with desktop and mobile responsive layouts.
- Dynamic layer management: Static Susceptibility (baseline terrain/drainage model), Historical Flood Hotspots, Community Reports (verified vs. unverified), Road Network Exposure (key corridors/subways).
- Hyperlocal Location Risk Inspection: On-click querying of coordinates and designated road segments returning risk tier, component features (elevation, slope, distance to storm outfall, rainfall), and explicit uncertainty metrics.
- Participatory Flood Reporting Workflow: Mobile-first report submission (category, estimated depth range, road passability, optional image upload, privacy consent).
- Moderation / Review Dashboard: Authorization-protected review queue for verification, tagging, and audit trail of community reports.
- Machine Learning Pipeline:
  - Standardized tabular geospatial dataset builder for Mumbai study area.
  - Reproducible Flood Susceptibility Baseline (Random Forest / Gradient Boosted Trees) evaluated with spatial and holdout splits.
  - Uncertainty quantification and calibration metrics (Brier score, PR-AUC).
- Fallback & Demo Mode: Explicitly labeled synthetic demo fixture mode when live meteorological APIs or external sensors are unavailable, guaranteeing honest presentation.
- Complete REST API with OpenAPI documentation (`/api/v1/*`), database migrations, unit/integration/ML tests.

### 4.2 Out-of-Scope (Post-MVP Roadmap)

- Real-time automated hydrodynamic 2D shallow-water numerical modeling (e.g., SWMM/HEC-RAS real-time physics engines).
- Real-time automatic Sentinel-1 interferometric synthetic aperture radar (InSAR) coherence processing on the fly (handled via pre-computed scenes/baselines in MVP).
- Direct integration with emergency dispatch 112 / sirens without municipal statutory approvals.
- Turn-by-turn live navigation rerouting algorithms.

---

## 5. Functional Requirements

| Requirement ID | Module | Title | Description | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Map | View Geographic Flood-Risk Map | Interactive vector/raster map of Mumbai with smooth pan/zoom and layer toggling. | Renders basemap centered on Mumbai (19.0760° N, 72.8777° E), supports zoom 10–18, renders susceptibility and observation layers within 2s. |
| **FR-002** | Map / Risk | Inspect Location Risk | Click anywhere on the study area or select a road segment to view risk profile. | Returns elevation, slope, terrain position, calculated susceptibility tier, and uncertainty flag. Shows "data unavailable" outside study area. |
| **FR-003** | Map / Meta | Source Freshness & Timestamps | Display data timestamps, model version, and last refresh time for all active layers. | UI badge indicates: Live / Stale / Demo Mode; displays UTC and IST timestamps of latest model run. |
| **FR-004** | Reports | Submit Community Flood Report | Public form allowing users to submit geo-tagged flood reports with category, water depth, and road status. | Validates lat/long within study area bounds, requires privacy consent, assigns UNVERIFIED status, persists to database. |
| **FR-005** | Reports | Review & Moderate Reports | Authorized review queue to verify, reject with reason, or mark reports duplicate. | Admin can view queue, update status to VERIFIED or REJECTED with notes; updates map marker status in real time. |
| **FR-006** | Historical | View Historical Flood Observations | Interface to inspect past monsoon flood events (e.g., July 2005, August 2017, July 2021, July 2023). | Displays historical rainfall totals, recorded waterlogging locations, and comparison with susceptibility baseline. |
| **FR-007** | API | Documented REST API | Public and authenticated REST endpoints under `/api/v1` with OpenAPI/Swagger docs. | OpenAPI schema served at `/docs`; supports all standard queries with input validation and typed responses. |
| **FR-008** | ML / UX | Model Confidence & Limitations | Clear communication of prediction uncertainty and physical limitations. | Never outputs single uncalibrated percentage without confidence interval or limitation note (e.g., "Drainage blockage proxy not observed"). |
| **FR-009** | Map | Filter Observations by Time & Category | Controls to filter community reports and historical events by date range, severity, and passability. | Map updates markers dynamically based on selected filters without full page reload. |
| **FR-010** | Export | Export Authorized Data | Export GeoJSON / CSV of verified flood observations and model evaluation summaries for research. | Generates standards-compliant GeoJSON with CRS EPSG:4326; strips PII from community reports before export. |
| **FR-011** | System | Demo / Offline Mode Toggle | Explicit toggle between live external data connection and labeled synthetic demo fixtures. | Prominently banners the interface with "DEMO MODE (SYNTHETIC FIXTURES)" when active; zero simulated live data confusion. |

---

## 6. Non-Functional Requirements

### 6.1 Performance & Scalability

- Map layer rendering response time < 1.5 seconds under standard broadband/4G.
- API response time for point risk queries < 200 ms (p95).
- Database spatial indexing (R-Tree / GiST / Spatialite) on all spatial tables.

### 6.2 Scientific & ML Integrity

- Zero data fabrication: Test metrics and validation splits must be computed from actual validation sets or clearly separated synthetic benchmarks.
- Evaluation split protocol: Spatial holdout (e.g., Western Suburbs vs. Island City) and temporal holdout (monsoon season holdout).
- Model transparency: Models must report Brier score, PR-AUC, Precision@K, and feature importance.

### 6.3 Security & Privacy

- Zero credential leaks: Secrets managed strictly via environment variables.
- Privacy in Participatory Mapping: Community report coordinates can be fuzzed/jittered by 50m for residential locations; author names/IPs are hashed and never publicly exposed.
- Input sanitization: Strict MIME-type checking and file size capping (max 5 MB) for report photo uploads.
- CSRF & Rate limiting on report submissions (max 10 submissions per IP per 10 minutes).

### 6.4 Accessibility & UI Standards

- WCAG 2.1 AA compliance: Contrast ratio >= 4.5:1 for standard text.
- Never use color alone to communicate risk: Always pair color coding with high-contrast text labels (e.g., "High Risk", "Moderate", "Low") and accessible icons.
- Keyboard navigable controls and screen-reader accessible ARIA tags.

---

## 7. Data & Environmental Requirements

- **Spatial Reference System (CRS):** Primary storage and API interchange in WGS 84 (`EPSG:4326`). Metric distance calculations and hydrological slope computations in UTM Zone 43N (`EPSG:32643`).
- **Elevation Data:** NASA SRTM 30m / Copernicus DEM 30m.
- **Meteorological Data:** IMD (India Meteorological Department) station observations proxy, CHIRPS rainfall, and Open-Meteo precipitation archives.
- **Infrastructure:** OpenStreetMap road network and railway lines for Mumbai.
- **Study Area Extent (Mumbai MMR Bounding Box):**
  - Minimum Longitude: 72.75° E
  - Maximum Longitude: 73.05° E
  - Minimum Latitude: 18.85° N
  - Maximum Latitude: 19.30° N

---

## 8. Success Metrics

1. **Model Baseline:** Susceptibility baseline achieving PR-AUC >= 0.78 and Brier score <= 0.15 on spatially held-out test wards.
2. **Operational Utility:** Identification of 100% of historically persistent critical waterlogging subways (Milan, Andheri, Malad, Khar, Hindmata).
3. **Data Integrity:** 0 uncalibrated or unverified community reports displayed as verified ground truth.
4. **Developer Experience:** 100% automated test passing rate, zero-configuration local demo mode.
