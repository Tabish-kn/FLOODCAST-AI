# Engineering & Scientific Rulebook: FloodCast AI

This document establishes strict engineering, scientific, geospatial, and privacy rules for the FloodCast AI codebase and all contributors.

---

## 1. General Engineering Rules

1. **Inspect Before Modifying:** Always inspect existing code and file structures before editing. Preserve existing documentation, comments, and working tests.
2. **Small, Testable Iterations:** Make focused, verifiable changes. Every milestone must be accompanied by relevant unit or integration tests.
3. **No Hardcoded Secrets or Credentials:** Passwords, API tokens, secret keys, and personal data must be loaded exclusively from environment variables or `.env` files. Provide a clean `.env.example` with placeholders.
4. **Zero-Dependency Local DX:** Never require external proprietary software or running daemons for basic local tests and dev runs. Provide seamless fallback abstractions (e.g., SQLite spatial abstraction when PostgreSQL/PostGIS is absent).
5. **No Silent Replacements with Placeholders:** Never replace working code or functional implementations with non-functional `TODO` or placeholder stubs.
6. **No Phantom Claims:** Never claim a test has passed, an API has executed, or a model has been trained unless you have directly verified the command output.
7. **Type Safety & Structured Validation:** Use strict Pydantic v2 schemas for all backend API endpoints and TypeScript interfaces for all frontend contracts.
8. **Semantic Error Responses:** Use RFC-7807 compliant structured JSON error payloads with clear error codes, helpful messages, and debug hints.

---

## 2. Machine Learning & Scientific Integrity Rules

1. **Never Fabricate Data or Metrics:** Under zero circumstances may training labels, synthetic sensor readings, or model evaluation metrics (e.g., PR-AUC, Brier score) be fabricated or inflated to look good in the UI.
2. **Missing Reports $\neq$ Absence of Flooding:** Never treat areas with zero community reports as confirmed dry or zero-risk zones. Always communicate: *"Absence of reports does not imply absence of waterlogging."*
3. **Strict Temporal & Spatial Separation:**
   - **No Future Leakage:** Never allow future rainfall or post-event observations to enter historical feature vectors for forecasting.
   - **Spatial Holdouts:** Evaluate model generalization across distinct geographic wards (e.g., train on Suburbs, hold out Island City) rather than using naive random pixel/point splits that leak spatial autocorrelation.
   - **Event Holdouts:** Evaluate on entirely held-out monsoon flood dates.
4. **Calibrated Probabilities:** Raw classification probabilities from tree ensembles or neural networks must be calibrated (e.g., using isotonic regression or Platt scaling) before being communicated as operational probabilities.
5. **Uncertainty & Limitations:** Every prediction output must include explicit uncertainty indicators and documented physical limitations (e.g., unmeasured local storm drain blockage).
6. **No Emergency Response Claims Without Authorization:** FloodCast AI is a decision-support and research platform. Never make statutory emergency dispatch claims without municipal authorization.

---

## 3. Geospatial Integrity Rules

1. **Explicit Coordinate Reference Systems (CRS):** Always document and enforce the CRS. Internal storage and GeoJSON transmission must adhere strictly to `EPSG:4326` (WGS 84). Metric distance and hydrological calculations must project explicitly to UTM Zone 43N (`EPSG:32643`).
2. **Validate Geometries & Bounds:** Validate all incoming latitude/longitude pairs against the study area bounding box for Mumbai:
   - Longitude: `[72.75, 73.05]`
   - Latitude: `[18.85, 19.30]`
3. **Micro-Drainage Caveat:** Global or regional DEMs (SRTM 30m, Copernicus 30m) do not resolve micro-topographic street gutters, storm curb inlets, or flyover underpasses. Always communicate spatial resolution and positional uncertainty.
4. **Safe Road Passage Disclaimer:** A low flood-risk score on a road segment does not guarantee safe vehicular passage; physical debris, manhole displacement, or power cable hazards may still exist.

---

## 4. Privacy & Participatory Mapping Rules

1. **Data Minimization:** Collect only necessary report metadata (location, observation time, depth range, road status). Do not require full names, phone numbers, or social identities for public reporting.
2. **Residential Location Protection:** Provide automated location fuzzing (jittering coordinates by ~50 meters) when a user flags a report as residential.
3. **Image Privacy & Sanitization:** Automatically strip EXIF metadata (including embedded GPS and device serials) from uploaded photos before saving to disk or object storage.
4. **Provenance & Verification Tracking:**
   - Never display an unverified community report as a verified observation.
   - Distinct visual symbols and statuses (`PENDING`, `VERIFIED`, `REJECTED`, `DUPLICATE`) must be enforced across all API endpoints and map views.
   - Never penalize or delete a report merely because it contradicts the current ML model output; community disagreement is critical research signal.
