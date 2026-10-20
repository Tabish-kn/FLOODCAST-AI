export interface HydrologicalFeatures {
  elevation_m: number;
  slope_degrees: number;
  distance_to_waterway_m: number;
  distance_to_storm_outfall_m: number;
  impervious_surface_fraction: number;
  historical_waterlogging_frequency: number;
  is_depression: boolean;
}

export interface UncertaintyMeta {
  confidence_tier: 'HIGH' | 'MODERATE' | 'LOW';
  is_calibrated: boolean;
  data_freshness: 'LIVE' | 'STALE' | 'DEMO_MODE';
  missing_proxies: string[];
  limitations_note: string;
}

export interface PredictionResult {
  prediction_id: string;
  target_type: string;
  latitude: number;
  longitude: number;
  risk_score: number;
  risk_tier: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  issue_time: string;
  target_window: string;
  model_version: string;
  features: HydrologicalFeatures;
  supporting_observations_count: number;
  nearby_subway_status?: string | null;
  uncertainty: UncertaintyMeta;
  demo_mode: boolean;
}

export interface CommunityReport {
  id: string;
  latitude: number;
  longitude: number;
  observation_time: string;
  category: string;
  depth_range: string;
  road_passability: string;
  image_url?: string | null;
  verification_status: 'UNVERIFIED' | 'VERIFIED' | 'REJECTED';
  notes?: string | null;
  created_at: string;
}

export interface RoadSegment {
  id: string;
  name: string;
  highway_type: string;
  is_subway: boolean;
  elevation_m: number;
  historical_vulnerability: string;
  line_geojson: {
    type: string;
    coordinates: number[][];
  };
}

export interface FloodObservation {
  id: string;
  location_name: string;
  latitude: number;
  longitude: number;
  water_depth_cm?: number | null;
  observation_source: string;
  confidence: string;
  recorded_at: string;
}

export interface FloodEvent {
  id: string;
  name: string;
  event_date: string;
  total_rainfall_mm: number;
  peak_intensity_mm_h: number;
  description?: string | null;
  observations: FloodObservation[];
}

export interface LayerMetadata {
  id: string;
  name: string;
  category: string;
  status: 'AVAILABLE' | 'UNAVAILABLE' | 'STALE';
  description: string;
  geometry_type: string;
  freshness: string;
  is_default_visible: boolean;
}
