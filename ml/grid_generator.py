"""Generates the canonical Mumbai flood susceptibility GeoJSON grid for MapLibre."""

import json
from pathlib import Path
from ml.inference import predict_location_risk

TIER_COLORS = {
    "LOW": "#10b981",       # Emerald
    "MODERATE": "#f59e0b",  # Amber
    "HIGH": "#f97316",      # Orange
    "CRITICAL": "#ef4444",  # Rose-Red
}


def generate_mumbai_susceptibility_grid(
    lat_min: float = 18.89,
    lat_max: float = 19.28,
    lon_min: float = 72.80,
    lon_max: float = 72.96,
    step_deg: float = 0.016,  # approx 1.7 km grid cell
) -> dict:
    features = []
    lat = lat_min

    cell_idx = 1
    while lat < lat_max:
        lon = lon_min
        while lon < lon_max:
            center_lat = lat + step_deg / 2.0
            center_lon = lon + step_deg / 2.0

            # Run inference for cell center
            pred = predict_location_risk(center_lat, center_lon, demo_mode=True)
            tier = pred["risk_tier"]
            score = pred["risk_score"]
            elev = pred["features"]["elevation_m"]
            slope = pred["features"]["slope_degrees"]

            # Cell polygon
            poly = [
                [round(lon, 4), round(lat, 4)],
                [round(lon + step_deg, 4), round(lat, 4)],
                [round(lon + step_deg, 4), round(lat + step_deg, 4)],
                [round(lon, 4), round(lat + step_deg, 4)],
                [round(lon, 4), round(lat, 4)],
            ]

            features.append({
                "type": "Feature",
                "id": f"cell-{cell_idx}",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [poly],
                },
                "properties": {
                    "cell_id": f"cell-{cell_idx}",
                    "center_lat": round(center_lat, 4),
                    "center_lon": round(center_lon, 4),
                    "risk_tier": tier,
                    "risk_score": score,
                    "elevation_m": elev,
                    "slope_degrees": slope,
                    "color": TIER_COLORS[tier],
                    "opacity": 0.65,
                },
            })
            cell_idx += 1
            lon += step_deg
        lat += step_deg

    geojson = {
        "type": "FeatureCollection",
        "name": "Mumbai Flood Susceptibility Grid (v1.0)",
        "features": features,
    }
    return geojson


def save_grid_fixture(output_path: str = "data/fixtures/mumbai_susceptibility_grid.geojson"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    grid = generate_mumbai_susceptibility_grid()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(grid, f, indent=2)
    print(f"Generated {len(grid['features'])} grid cells saved to {output_path}")


if __name__ == "__main__":
    save_grid_fixture()
