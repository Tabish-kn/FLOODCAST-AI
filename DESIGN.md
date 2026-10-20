# UI/UX Design Specification: FloodCast AI

## 1. Design Principles & Brand Identity

FloodCast AI is a scientific, decision-support environmental intelligence platform. The user interface prioritizes clarity, data transparency, rapid spatial comprehension, and accessibility over decorative visual fluff.

### 1.1 Core Principles

1. **Map-Centric Intelligence:** The geographic context of Mumbai is the primary canvas; information panels and controls frame and elevate the map without obscuring critical spatial features.
2. **Never Color Alone:** Flood risk and operational status must always be communicated using a triple combination: **Color + High-Contrast Text Label + Distinctive Shape/Icon**.
3. **Transparent Uncertainty:** The UI never displays single uncalibrated percentage scores without context. Data freshness, confidence intervals, and missing proxy warnings are always visible.
4. **Actionable for Logistics & Citizens:** Critical data (such as road impassability and subway waterlogging) is prioritized with prominent visual cues.
5. **Calm, High-Contrast Climate-Tech Aesthetic:** Sleek, modern dark/light mode with curated HSL color tokens, glassmorphic headers, crisp typography, and micro-interactions.

---

## 2. Color Palette & Theming

### 2.1 Color Tokens (Dark Mode by Default for Geospatial Visuals)

| Token Name | Hex Code | HSL | Usage |
| :--- | :--- | :--- | :--- |
| `--bg-primary` | `#0b0f19` | `223°, 41%, 7%` | Main canvas background, deep slate-navy |
| `--bg-surface` | `#111827` | `222°, 36%, 11%` | Cards, sidebars, modals |
| `--bg-surface-elevated` | `#1f2937` | `217°, 33%, 17%` | Hover states, dropdown menus, borders |
| `--text-primary` | `#f9fafb` | `210°, 20%, 98%` | Primary headers, high-contrast values |
| `--text-secondary` | `#9ca3af` | `218°, 11%, 65%` | Labels, subtitles, metadata |
| `--text-muted` | `#6b7280` | `220°, 9%, 46%` | Inactive elements, helper text |
| `--border-subtle` | `#374151` | `217°, 19%, 27%` | Dividers, card borders, input borders |
| `--accent-cyan` | `#06b6d4` | `189°, 94%, 43%` | Primary brand accent, selected nodes |
| `--accent-blue` | `#3b82f6` | `217°, 91%, 60%` | Waterbodies, normal precipitation |

### 2.2 Standardized Risk Palette (Triple-Encoded)

| Tier | Color | Hex | Visual Symbol | Text Label | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Low / Minimal** | Emerald | `#10b981` | Circle (●) | **LOW RISK** | High elevation (>15m), steep drainage slope, zero historical waterlogging. |
| **Moderate** | Amber | `#f59e0b` | Diamond (◆) | **MODERATE** | Low elevation (5–15m), mild slope, susceptible during extreme downpours. |
| **High** | Orange | `#f97316` | Triangle (▲) | **HIGH RISK** | Low depression (<5m), proximity to tidal outfall, documented recurrent logging. |
| **Severe / Critical** | Rose-Red | `#ef4444` | Octagon (🛑) | **CRITICAL** | Severe waterlogging, subway closure, deep water entering structures. |
| **Unknown / Missing** | Slate | `#64748b` | Question Mark (?) | **NO DATA** | Outside active study area boundary or sensor telemetry missing. |

---

## 3. Typography & Hierarchy

FloodCast AI uses modern system-first typography paired with clean, geometric sans-serif fonts:

- **Primary Font Family:** `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Monospace Font Family:** `'JetBrains Mono', 'Fira Code', 'Courier New', monospace` (for coordinates, timestamps, and model hashes)

### Scale

- **H1 / Page Title:** 24px / 1.3 line-height / Semi-bold (600)
- **H2 / Section Title:** 18px / 1.35 line-height / Semi-bold (600)
- **H3 / Card Header:** 15px / 1.4 line-height / Medium (500)
- **Body Text:** 14px / 1.5 line-height / Regular (400)
- **Caption / Metadata:** 12px / 1.4 line-height / Regular (400)
- **Badges / Micro-labels:** 11px / 1.2 line-height / Bold (700) / Uppercase

---

## 4. Spacing, Layout & Navigation

### 4.1 Global Layout

- **Header Bar (Top, 60px):** Brand logo, Mumbai Study Area badge, Data Freshness status, Mode indicator (Demo / Live), Nav links, Theme switch.
- **Main Viewport (Full height):**
  - Left / Main Canvas: MapLibre interactive canvas with floating layer controller and zoom pills.
  - Right Collapsible Panel (380px desktop, full-width sheet on mobile): Selected location risk profile, component features, nearby reports, and action buttons.
- **Floating Bottom Bar / Drawer:** Mobile navigation and quick "Submit Report" floating action button (FAB).

### 4.2 Spacing System

Follows an 8-point harmonic grid:

- `space-1`: 4px
- `space-2`: 8px
- `space-3`: 12px
- `space-4`: 16px
- `space-6`: 24px
- `space-8`: 32px

---

## 5. Map Design & Layer Visual Language

Map layers are visually distinct and mutually non-interfering:

### 5.1 Layer Visual Matrix

| Layer Category | Geometry Type | Representation | Opacity & Style |
| :--- | :--- | :--- | :--- |
| **Static Susceptibility** | Hexagonal Grid / Polygons | Continuous gradient (Emerald $\rightarrow$ Amber $\rightarrow$ Rose) | 0.65 fill opacity, smooth bilinear styling |
| **Historical Hotspots** | Point Clusters / Buffer Circles | Deep indigo circle with waterdrop icon | Stroke `#ffffff`, radius 8–18px based on zoom |
| **Community Reports (Unverified)** | Pulsing Outline Marker | Amber hollow circle with dash outline (⬚) | High contrast, distinct from verified markers |
| **Community Reports (Verified)** | Solid Verified Marker | Teal filled circle with white checkmark (✓) | High contrast, 12px diameter |
| **Road Network Exposure** | LineString segments | Solid colored lines with dashed casing for subways | Width 3px–6px depending on zoom |
| **Study Area Boundary** | Polygon Outline | Bright cyan dashed border | 1.5px stroke, no fill |

---

## 6. Location Risk Inspector Panel

When a user clicks any location or road segment on the map, the inspector renders:

```text
+------------------------------------------------------+
| 📍 SELECTED LOCATION: Kurla West / Mithi Corridor    |
| Coordinates: 19.0682° N, 72.8791° E  [Elev: 4.2m]     |
+------------------------------------------------------+
| RISK ASSESSMENT:                                     |
| [ ▲ HIGH RISK ]  Confidence: Moderate (0.84 calibrated) |
+------------------------------------------------------+
| CONTRIBUTING HYDROLOGICAL FACTORS:                  |
| - Terrain Elevation: 4.2m (Low Depression)           |
| - Slope: 0.3° (Poor gravitational runoff)            |
| - Distance to Tidal Outfall: 340m (High tide choke)  |
| - Impervious Area: 88% (Dense urban concrete)        |
+------------------------------------------------------+
| SUPPORTING GROUND EVIDENCE:                          |
| ⚠️ 3 Verified community reports within 400m          |
| 🕒 Last reported: 22 mins ago ("Waterlogging 1.5ft") |
+------------------------------------------------------+
| MODEL LIMITATIONS & UNCERTAINTY:                     |
| Note: Local storm drain maintenance state unobserved. |
| Model: v1.0-rf-mumbai | Issue Time: 2026-10-20 17:30 |
+------------------------------------------------------+
```

---

## 7. Participatory Reporting Flow (Mobile & Desktop)

### 7.1 Submission Modal / Form Flow

1. **Location Confirmation:** Automatically drops a pin at user's current GPS location or clicked map point (with latitude/longitude coordinate badge and reverse-geocoded landmark).
2. **Category Selection:**
   - 💧 Minor Waterlogging (< 0.5 ft)
   - 🌊 Significant Waterlogging (0.5 – 1.5 ft)
   - 🚗 Road Impassable / Subway Flooded (> 1.5 ft)
   - 🏢 Water Ingress into Buildings
   - 🚯 Storm Drain Overflow / Blocked Gutter
3. **Road Passability Status:** Radio buttons for `Passable for all`, `Two-wheelers only`, `Heavy vehicles only`, `Completely Impassable`.
4. **Estimated Water Depth:** Slider or discrete chips (`<6 in`, `6-12 in`, `1-2 ft`, `>2 ft`, `Unknown`).
5. **Optional Image:** Drag & drop / camera snap with EXIF privacy stripping notice.
6. **Privacy & Consent Notice:** Mandatory checkbox: *"I understand this report is publicly visible without personal details to help inform commuters and research."*
7. **Submission Feedback:** Immediate green toast notification with assigned Report Tracking ID and badge stating `"Pending Verification"`.

---

## 8. State Indicators & Honest Communication

### 8.1 Data Freshness Badge

- 🟢 **LIVE:** Real-time data feed updated within the past 60 minutes.
- 🟡 **STALE:** Feed delayed > 60 minutes; displays actual timestamp of last received observation.
- 🔵 **DEMO MODE:** Clearly labeled banner at the top of the interface: *"Active Mode: Synthetic Demonstration Fixtures for Mumbai. No external live sensor connected."*

### 8.2 Empty, Loading & Error States

- **Loading State:** Skeleton shimmers on cards; semi-transparent spinner over map tile canvas with text *"Querying hydrological grid..."*.
- **Empty State:** Distinct illustrated message: *"No flood reports in this ward for the selected time window. This indicates an absence of recorded reports, not guaranteed dry conditions."*
- **Error State:** Dismissible alert banner explaining the exact cause (e.g., *"Unable to reach prediction service. Retrying in 5 seconds..."*) with a manual "Retry Now" button.

---

## 9. Accessibility & Responsiveness

- High color contrast ratio (minimum 4.8:1 on all text elements).
- Full keyboard support: `Tab` to navigate controls, `Esc` to close inspector panels/modals, `Arrow` keys for map panning when map container is focused.
- Screen-reader tags: All risk badges and icons have descriptive `aria-label` attributes (e.g., `aria-label="High Risk Level: Low elevation depression with poor drainage"`).
- Mobile layout converts side panel into an accessible bottom sheet with touch-drag dismissal.
