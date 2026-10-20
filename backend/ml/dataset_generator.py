"""Dataset generator for FloodCast AI benchmark experiments."""

import random
import pandas as pd
import numpy as np
from typing import Tuple
from ml.features import (
    compute_hydrological_features,
    HISTORIC_DEPRESSIONS,
    ELEVATED_CENTERS,
)

# Seed for absolute reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def generate_benchmark_dataset(n_samples: int = 1200) -> pd.DataFrame:
    """
    Generates a structured, realistic geospatial dataset of points across Mumbai.
    Includes known historical waterlogged points, random urban points, and elevated controls.
    """
    rows = []

    # 1. Add known historical flood hotspots with slight spatial jitter
    for dep in HISTORIC_DEPRESSIONS:
        for _ in range(25):
            # Jitter within 300 meters
            lat = dep["lat"] + random.gauss(0, 0.0015)
            lon = dep["lon"] + random.gauss(0, 0.0015)
            feats = compute_hydrological_features(lat, lon)
            # High flood label = 1
            rows.append({
                "latitude": lat,
                "longitude": lon,
                "ward_region": "Island City" if lat < 19.05 else ("Western Suburbs" if lon < 72.88 else "Eastern Suburbs"),
                **feats,
                "is_flooded": 1,
                "event_year": random.choice([2017, 2019, 2021, 2023]),
                "sample_type": "HOTSPOT",
            })

    # 2. Add elevated non-flood controls
    for hill in ELEVATED_CENTERS:
        for _ in range(20):
            lat = hill["lat"] + random.gauss(0, 0.003)
            lon = hill["lon"] + random.gauss(0, 0.003)
            feats = compute_hydrological_features(lat, lon)
            rows.append({
                "latitude": lat,
                "longitude": lon,
                "ward_region": "Island City" if lat < 19.05 else ("Western Suburbs" if lon < 72.88 else "Eastern Suburbs"),
                **feats,
                "is_flooded": 0,
                "event_year": random.choice([2017, 2019, 2021, 2023]),
                "sample_type": "ELEVATED_CONTROL",
            })

    # 3. Add random urban points across Mumbai bounds
    while len(rows) < n_samples:
        lat = random.uniform(18.90, 19.28)
        lon = random.uniform(72.80, 72.96)
        feats = compute_hydrological_features(lat, lon)

        # Ground truth rule based on physical hydrology
        # Floods occur primarily if elevation < 4m AND (slope < 0.8 OR near outfall) AND high impervious
        prob_flood = 0.05
        if feats["elevation_m"] < 3.5:
            prob_flood += 0.50
        elif feats["elevation_m"] < 5.0:
            prob_flood += 0.25
        elif feats["elevation_m"] > 15.0:
            prob_flood = 0.01

        if feats["slope_degrees"] < 0.5:
            prob_flood += 0.20
        if feats["distance_to_storm_outfall_m"] < 1000:
            prob_flood += 0.15

        prob_flood = min(0.95, max(0.01, prob_flood))
        is_flooded = 1 if random.random() < prob_flood else 0

        rows.append({
            "latitude": lat,
            "longitude": lon,
            "ward_region": "Island City" if lat < 19.05 else ("Western Suburbs" if lon < 72.88 else "Eastern Suburbs"),
            **feats,
            "is_flooded": is_flooded,
            "event_year": random.choice([2017, 2019, 2021, 2023]),
            "sample_type": "RANDOM_URBAN",
        })

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = generate_benchmark_dataset(1500)
    output_path = "data/processed/mumbai_flood_benchmark.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated benchmark dataset with {len(df)} samples saved to {output_path}")
    print("Class distribution:")
    print(df["is_flooded"].value_counts(normalize=True))
    print("Wards distribution:")
    print(df["ward_region"].value_counts())
