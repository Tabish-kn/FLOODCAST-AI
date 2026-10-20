import React from 'react';
import { X, AlertCircle, ShieldAlert, CheckCircle2, Waves, Droplet, ArrowUpRight, Compass } from 'lucide-react';
import type { PredictionResult } from '../types';



interface RiskInspectorPanelProps {
  prediction: PredictionResult | null;
  loading: boolean;
  onClose: () => void;
  onOpenReportModal: (lat: number, lon: number) => void;
}

export const RiskInspectorPanel: React.FC<RiskInspectorPanelProps> = ({
  prediction,
  loading,
  onClose,
  onOpenReportModal,
}) => {
  if (loading) {
    return (
      <div className="risk-inspector-panel">
        <div className="inspector-header">
          <div>
            <div className="inspector-title">Analyzing Location...</div>
            <div className="inspector-coords">Querying hydrological terrain grid</div>
          </div>
          <button className="close-btn" onClick={onClose}><X size={18} /></button>
        </div>
        <div className="inspector-body" style={{ alignItems: 'center', justifyContent: 'center', height: '60%' }}>
          <div style={{ color: 'var(--accent-cyan)', fontSize: 14 }}>Calculating calibrated risk profile...</div>
        </div>
      </div>
    );
  }

  if (!prediction) return null;

  const { risk_tier, risk_score, features, uncertainty, nearby_subway_status } = prediction;

  const getTierIcon = () => {
    switch (risk_tier) {
      case 'CRITICAL': return <ShieldAlert size={22} color="#ef4444" />;
      case 'HIGH': return <AlertCircle size={22} color="#f97316" />;
      case 'MODERATE': return <Compass size={22} color="#f59e0b" />;
      default: return <CheckCircle2 size={22} color="#10b981" />;
    }
  };

  return (
    <div className="risk-inspector-panel">
      {/* Header */}
      <div className="inspector-header">
        <div>
          <div className="inspector-title">Location Risk Profile</div>
          <div className="inspector-coords">
            {prediction.latitude.toFixed(4)}° N, {prediction.longitude.toFixed(4)}° E
          </div>
        </div>
        <button className="close-btn" onClick={onClose} title="Close inspector">
          <X size={18} />
        </button>
      </div>

      <div className="inspector-body">
        {/* Triple-Encoded Risk Hero Card */}
        <div className={`risk-hero-card ${risk_tier}`}>
          <div>
            <div style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', opacity: 0.8 }}>
              Assessed Flood Risk Tier
            </div>
            <div className="risk-tier-label" style={{ marginTop: 4 }}>
              {getTierIcon()}
              <span>{risk_tier} RISK</span>
            </div>
            <div style={{ fontSize: 12, marginTop: 4, opacity: 0.85 }}>
              Confidence: <strong>{uncertainty.confidence_tier}</strong>
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', opacity: 0.8 }}>
              Calibrated Prob.
            </div>
            <div className="risk-probability-badge">
              {(risk_score * 100).toFixed(1)}%
            </div>
          </div>
        </div>

        {/* Nearby Vulnerable Subway Alert */}
        {nearby_subway_status && (
          <div style={{
            background: 'rgba(239, 68, 68, 0.12)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: 'var(--radius-md)',
            padding: '12px 14px',
            display: 'flex',
            alignItems: 'center',
            gap: 10,
          }}>
            <Waves size={20} color="#ef4444" />
            <div>
              <div style={{ fontSize: 12, fontWeight: 700, color: '#fca5a5' }}>Critical Underpass Proximity</div>
              <div style={{ fontSize: 12, color: 'var(--text-primary)' }}>{nearby_subway_status}</div>
            </div>
          </div>
        )}

        {/* Hydrological Features Breakdown */}
        <div>
          <div style={{ fontSize: 12, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: 10 }}>
            Contributing Physical Factors
          </div>
          <div className="feature-metric-grid">
            <div className="metric-card">
              <div className="metric-label">Elevation</div>
              <div className="metric-value">{features.elevation_m} m ASL</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Local Slope</div>
              <div className="metric-value">{features.slope_degrees}°</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Tidal Outfall Dist</div>
              <div className="metric-value">
                {features.distance_to_storm_outfall_m > 1000
                  ? `${(features.distance_to_storm_outfall_m / 1000).toFixed(1)} km`
                  : `${Math.round(features.distance_to_storm_outfall_m)} m`}
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Impervious Surface</div>
              <div className="metric-value">{Math.round(features.impervious_surface_fraction * 100)}%</div>
            </div>
          </div>
        </div>

        {/* Scientific Limitations & Uncertainty */}
        <div className="limitations-box">
          <div style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 4, display: 'flex', alignItems: 'center', gap: 6 }}>
            <Droplet size={14} color="#06b6d4" />
            <span>Scientific Limitations &amp; Freshness</span>
          </div>
          <div>{uncertainty.limitations_note}</div>
          <div style={{ marginTop: 8, fontSize: 11, color: 'var(--text-muted)' }}>
            Model: <strong>{prediction.model_version}</strong> | Data Mode: <strong>{uncertainty.data_freshness}</strong>
          </div>
        </div>

        {/* Action Button: Report Waterlogging here */}
        <button
          className="btn-primary"
          onClick={() => onOpenReportModal(prediction.latitude, prediction.longitude)}
        >
          <span>Report Waterlogging at This Pin</span>
          <ArrowUpRight size={16} />
        </button>
      </div>
    </div>
  );
};
