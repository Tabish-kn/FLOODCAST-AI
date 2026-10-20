"""Unit tests for geospatial bounds and hydrological feature calculations."""

import pytest
from ml.features import compute_hydrological_features, estimate_elevation_and_slope, haversine_distance_m


def test_haversine_distance():
    # Distance between Hindmata (19.0069, 72.8415) and Milan Subway (19.0888, 72.8427) ~ 9.1 km
    dist = haversine_distance_m(19.0069, 72.8415, 19.0888, 72.8427)
    assert 9000 < dist < 9300


def test_hindmata_features_depression():
    # Hindmata is a known low-lying historical depression
    feats = compute_hydrological_features(19.0069, 72.8415)
    assert feats["elevation_m"] < 4.0
    assert feats["slope_degrees"] < 1.0
    assert feats["is_depression"] == 1.0
    assert feats["historical_waterlogging_frequency"] >= 8


def test_malabar_hill_features_elevated():
    # Malabar Hill is elevated promontory > 40m
    feats = compute_hydrological_features(18.9560, 72.7980)
    assert feats["elevation_m"] > 35.0
    assert feats["is_depression"] == 0.0


def test_distance_to_outfall_positive():
    feats = compute_hydrological_features(19.0435, 72.8402)
    # Right on Mithi River Mahim Bay outfall
    assert feats["distance_to_storm_outfall_m"] < 100
