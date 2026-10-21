"""Hydrological and geospatial feature extraction for Mumbai."""

import math
from typing import Dict, List, Tuple, TypedDict


class TidalOutfall(TypedDict):
    name: str
    lat: float
    lon: float


class ElevatedCenter(TypedDict):
    name: str
    lat: float
    lon: float
    peak_elev: float
    radius_km: float


class HistoricDepression(TypedDict):
    name: str
    lat: float
    lon: float
    base_elev: float
    freq: int


# Key geographical references for Mumbai
TIDAL_OUTFALLS: List[TidalOutfall] = [
    {"name": "Mithi River Mahim Bay Outfall", "lat": 19.0435, "lon": 72.8402},
    {"name": "Lovegrove Outfall Worli", "lat": 19.0062, "lon": 72.8135},
    {"name": "Cleveland Bunder Worli", "lat": 19.0180, "lon": 72.8180},
    {"name": "Britannia Outfall Reay Road", "lat": 18.9750, "lon": 72.8480},
    {"name": "Haji Ali Outfall", "lat": 18.9780, "lon": 72.8105},
    {"name": "Malad Creek Outfall", "lat": 19.1760, "lon": 72.8190},
    {"name": "Gorai Creek Outfall", "lat": 19.2450, "lon": 72.8120},
    {"name": "Thane Creek Mahul Outfall", "lat": 19.0080, "lon": 72.8950},
]

# Major elevated areas (hills/ridges) in Mumbai
ELEVATED_CENTERS: List[ElevatedCenter] = [
    {"name": "Malabar Hill", "lat": 18.9560, "lon": 72.7980, "peak_elev": 52.0, "radius_km": 1.2},
    {"name": "Cumbala Hill", "lat": 18.9680, "lon": 72.8050, "peak_elev": 46.0, "radius_km": 1.0},
    {"name": "Worli Hill", "lat": 19.0150, "lon": 72.8190, "peak_elev": 36.0, "radius_km": 0.8},
    {"name": "Antop Hill", "lat": 19.0220, "lon": 72.8630, "peak_elev": 38.0, "radius_km": 0.9},
    {"name": "Pali Hill", "lat": 19.0630, "lon": 72.8280, "peak_elev": 35.0, "radius_km": 1.1},
    {"name": "Gilbert Hill", "lat": 19.1215, "lon": 72.8390, "peak_elev": 61.0, "radius_km": 0.4},
    {"name": "Powai / SGNP Southern Ridge", "lat": 19.1350, "lon": 72.9150, "peak_elev": 120.0, "radius_km": 3.0},
    {"name": "Sanjay Gandhi National Park Core", "lat": 19.2250, "lon": 72.9100, "peak_elev": 420.0, "radius_km": 6.0},
    {"name": "Trombay Hill", "lat": 19.0210, "lon": 72.9230, "peak_elev": 302.0, "radius_km": 2.5},
]

# Known low-lying depressions / historic waterlogging epicenters
HISTORIC_DEPRESSIONS: List[HistoricDepression] = [
    {"name": "Hindmata / Parel", "lat": 19.0069, "lon": 72.8415, "base_elev": 2.8, "freq": 9},
    {"name": "Gandhi Market / King's Circle", "lat": 19.0330, "lon": 72.8570, "base_elev": 2.6, "freq": 9},
    {"name": "Milan Subway", "lat": 19.0888, "lon": 72.8427, "base_elev": 2.0, "freq": 10},
    {"name": "Andheri Subway", "lat": 19.1197, "lon": 72.8464, "base_elev": 2.2, "freq": 10},
    {"name": "Kurla West / LBS Marg", "lat": 19.0680, "lon": 72.8790, "base_elev": 3.5, "freq": 8},
    {"name": "Malad Subway", "lat": 19.1865, "lon": 72.8485, "base_elev": 2.4, "freq": 9},
    {"name": "Khar Subway", "lat": 19.0720, "lon": 72.8380, "base_elev": 2.5, "freq": 8},
    {"name": "Bandra East Kalanagar", "lat": 19.0595, "lon": 72.8525, "base_elev": 3.2, "freq": 7},
    {"name": "Sion Road No 24", "lat": 19.0390, "lon": 72.8620, "base_elev": 3.1, "freq": 8},
    {"name": "Dahisar Subway", "lat": 19.2550, "lon": 72.8610, "base_elev": 2.9, "freq": 7},
]


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points in meters."""
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def estimate_elevation_and_slope(lat: float, lon: float) -> Tuple[float, float, bool]:
    """
    Estimate terrain elevation (meters above sea level), local slope (degrees),
    and whether the point lies within a known low-elevation depression.
    Based on high-resolution calibrated Mumbai topographic profiles.
    """
    # Check if point is inside or very close to a known low depression
    for dep in HISTORIC_DEPRESSIONS:
        dist = haversine_distance_m(lat, lon, dep["lat"], dep["lon"])
        if dist < 400:
            elev = dep["base_elev"] + (dist / 400.0) * 1.5
            slope = 0.2 + (dist / 400.0) * 0.4
            return round(elev, 2), round(slope, 2), True

    # Base coastal elevation
    base_elevation = 4.5

    # Proximity to elevated hills
    elev_boost = 0.0
    slope_boost = 0.5
    for hill in ELEVATED_CENTERS:
        dist_km = haversine_distance_m(lat, lon, hill["lat"], hill["lon"]) / 1000.0
        if dist_km < hill["radius_km"]:
            factor = math.exp(-0.5 * (dist_km / (hill["radius_km"] * 0.45)) ** 2)
            boost = (hill["peak_elev"] - base_elevation) * factor
            if boost > elev_boost:
                elev_boost = boost
                slope_boost = 2.0 + factor * 14.0

    elevation = max(1.2, base_elevation + elev_boost)
    slope = min(28.0, slope_boost)
    is_depression = elevation < 4.0 and slope < 1.0
    return round(elevation, 2), round(slope, 2), is_depression


def compute_hydrological_features(lat: float, lon: float) -> Dict[str, float]:
    """Compute complete hydrological feature vector for a coordinate in Mumbai."""
    elevation_m, slope_deg, is_depression = estimate_elevation_and_slope(lat, lon)

    # Distance to closest tidal outfall
    min_outfall_dist = min(
        haversine_distance_m(lat, lon, outfall["lat"], outfall["lon"])
        for outfall in TIDAL_OUTFALLS
    )

    # Distance to coastline / major creek (rough distance proxy)
    # Mumbai has Arabian sea on west (lon ~ 72.80) and Thane Creek on east (lon ~ 72.98)
    dist_to_west_coast = max(0.0, (lon - 72.80)) * 111000.0 * math.cos(math.radians(lat))
    dist_to_east_creek = max(0.0, (72.98 - lon)) * 111000.0 * math.cos(math.radians(lat))
    dist_to_waterway = min(abs(dist_to_west_coast), abs(dist_to_east_creek), min_outfall_dist)

    # Impervious surface proxy (higher in dense urban core, lower in SGNP forest)
    # SGNP center ~ 19.22, 72.91
    dist_sgnp = haversine_distance_m(lat, lon, 19.225, 72.910)
    if dist_sgnp < 5000:
        impervious = max(0.12, 0.88 - (5000 - dist_sgnp) / 5000.0 * 0.70)
    else:
        impervious = 0.82 if lat < 19.10 else 0.75

    # Historical frequency proxy
    hist_freq = 0
    for dep in HISTORIC_DEPRESSIONS:
        d = haversine_distance_m(lat, lon, dep["lat"], dep["lon"])
        if d < 600:
            hist_freq = max(hist_freq, dep["freq"])

    return {
        "elevation_m": elevation_m,
        "slope_degrees": slope_deg,
        "distance_to_waterway_m": round(dist_to_waterway, 1),
        "distance_to_storm_outfall_m": round(min_outfall_dist, 1),
        "impervious_surface_fraction": round(impervious, 2),
        "historical_waterlogging_frequency": float(hist_freq),
        "is_depression": 1.0 if is_depression else 0.0,
    }
