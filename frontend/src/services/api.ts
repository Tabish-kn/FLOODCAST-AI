import type {
  PredictionResult,
  CommunityReport,
  FloodEvent,
  LayerMetadata,
} from '../types';


const API_BASE = '/api/v1';

export async function fetchMapLayers(): Promise<{ layers: LayerMetadata[] }> {
  const res = await fetch(`${API_BASE}/map/layers`);
  if (!res.ok) throw new Error('Failed to fetch map layers');
  return res.json();
}

export async function fetchMapFeatures(layer: string): Promise<any> {
  const res = await fetch(`${API_BASE}/map/features?layer=${layer}`);
  if (!res.ok) throw new Error(`Failed to fetch features for layer: ${layer}`);
  return res.json();
}

export async function queryRisk(lat: number, lon: number): Promise<PredictionResult> {
  const res = await fetch(`${API_BASE}/predictions/query?lat=${lat}&lon=${lon}`);
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.message || 'Failed to inspect location risk');
  }
  return res.json();
}

export async function fetchReports(statusFilter: string = 'ALL'): Promise<CommunityReport[]> {
  const res = await fetch(`${API_BASE}/reports?status_filter=${statusFilter}`);
  if (!res.ok) throw new Error('Failed to fetch community reports');
  return res.json();
}

export async function submitReport(payload: {
  latitude: number;
  longitude: number;
  category: string;
  depth_range: string;
  road_passability: string;
  consent_granted: boolean;
  is_residential?: boolean;
}): Promise<CommunityReport> {
  const res = await fetch(`${API_BASE}/reports`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.message || 'Failed to submit report');
  }
  return res.json();
}

export async function reviewReport(
  reportId: string,
  decision: 'VERIFIED' | 'REJECTED' | 'DUPLICATE',
  reason: string,
): Promise<CommunityReport> {
  const res = await fetch(`${API_BASE}/reports/${reportId}/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ decision, reason, reviewer_id: 'chief-hydrology-reviewer' }),
  });
  if (!res.ok) throw new Error('Failed to submit review');
  return res.json();
}

export async function fetchFloodEvents(): Promise<FloodEvent[]> {
  const res = await fetch(`${API_BASE}/flood-events`);
  if (!res.ok) throw new Error('Failed to fetch flood events');
  return res.json();
}

export async function fetchModelMetrics(): Promise<any> {
  const res = await fetch(`${API_BASE}/models/metrics`);
  if (!res.ok) throw new Error('Failed to fetch model metrics');
  return res.json();
}
