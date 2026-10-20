import React, { useState } from 'react';
import { X, Send, ShieldCheck, MapPin } from 'lucide-react';
import { submitReport } from '../services/api';

interface ReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  defaultCoords: { lat: number; lon: number } | null;
  onReportSubmitted: () => void;
}

export const ReportModal: React.FC<ReportModalProps> = ({
  isOpen,
  onClose,
  defaultCoords,
  onReportSubmitted,
}) => {
  if (!isOpen) return null;

  const [lat, setLat] = useState(defaultCoords?.lat?.toFixed(5) || '19.0760');
  const [lon, setLon] = useState(defaultCoords?.lon?.toFixed(5) || '72.8777');
  const [category, setCategory] = useState('WATERLOGGING');
  const [depthRange, setDepthRange] = useState('6-12 in');
  const [roadPassability, setRoadPassability] = useState('PASSABLE');
  const [isResidential, setIsResidential] = useState(false);
  const [consentGranted, setConsentGranted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successId, setSuccessId] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!consentGranted) {
      setErrorMsg('You must grant consent to submit participatory mapping data.');
      return;
    }

    setLoading(true);
    setErrorMsg(null);

    try {
      const rep = await submitReport({
        latitude: parseFloat(lat),
        longitude: parseFloat(lon),
        category,
        depth_range: depthRange,
        road_passability: roadPassability,
        consent_granted: consentGranted,
        is_residential: isResidential,
      });

      setSuccessId(rep.id);
      onReportSubmitted();
      setTimeout(() => {
        onClose();
        setSuccessId(null);
      }, 1800);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to submit report.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <MapPin size={20} color="#06b6d4" />
            <h3 style={{ fontSize: 16, fontWeight: 700 }}>Submit Ground Flood Observation</h3>
          </div>
          <button className="close-btn" onClick={onClose}><X size={18} /></button>
        </div>

        {successId ? (
          <div className="modal-body" style={{ alignItems: 'center', textAlign: 'center', padding: '36px 24px' }}>
            <ShieldCheck size={48} color="#10b981" />
            <h4 style={{ fontSize: 18, fontWeight: 700, marginTop: 12 }}>Report Received!</h4>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>
              Tracking ID: <code>{successId}</code>
            </p>
            <div style={{
              background: 'rgba(245, 158, 11, 0.15)',
              color: '#f59e0b',
              padding: '6px 14px',
              borderRadius: 'var(--radius-full)',
              fontSize: 12,
              fontWeight: 600,
              marginTop: 10,
            }}>
              Status: UNVERIFIED (In Moderation Queue)
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="modal-body">
            {errorMsg && (
              <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', color: '#fca5a5', padding: '8px 12px', borderRadius: 6, fontSize: 13 }}>
                {errorMsg}
              </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <div className="form-group">
                <label className="form-label">Latitude (°N)</label>
                <input
                  type="number"
                  step="0.0001"
                  className="form-input"
                  value={lat}
                  onChange={(e) => setLat(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Longitude (°E)</label>
                <input
                  type="number"
                  step="0.0001"
                  className="form-input"
                  value={lon}
                  onChange={(e) => setLon(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Observation Category</label>
              <select
                className="form-select"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option value="WATERLOGGING">💧 Street Waterlogging</option>
                <option value="ROAD_IMPASSABLE">🚗 Road Impassable / Subway Flooded</option>
                <option value="DRAIN_OVERFLOW">🚯 Storm Drain / Gutter Overflow</option>
                <option value="WATER_ENTERING_BUILDING">🏢 Water Ingress into Structure</option>
                <option value="RECEDING">📉 Receding Floodwaters</option>
              </select>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <div className="form-group">
                <label className="form-label">Estimated Water Depth</label>
                <select
                  className="form-select"
                  value={depthRange}
                  onChange={(e) => setDepthRange(e.target.value)}
                >
                  <option value="<6 in">&lt; 6 inches (Ankle depth)</option>
                  <option value="6-12 in">6 - 12 inches (Shin depth)</option>
                  <option value="1-2 ft">1 - 2 feet (Knee depth)</option>
                  <option value=">2 ft">&gt; 2 feet (Waist depth / Submerged)</option>
                  <option value="UNKNOWN">Unknown / Unmeasured</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Road Passability</label>
                <select
                  className="form-select"
                  value={roadPassability}
                  onChange={(e) => setRoadPassability(e.target.value)}
                >
                  <option value="PASSABLE">Passable for All Vehicles</option>
                  <option value="TWO_WHEELERS_ONLY">Two-Wheelers Only</option>
                  <option value="HEAVY_ONLY">Heavy Vehicles / Buses Only</option>
                  <option value="IMPASSABLE">Completely Impassable</option>
                </select>
              </div>
            </div>

            {/* Privacy Location Fuzzing */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 4 }}>
              <input
                type="checkbox"
                id="residentialCheck"
                checked={isResidential}
                onChange={(e) => setIsResidential(e.target.checked)}
              />
              <label htmlFor="residentialCheck" style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
                Fuzz location by ~50m to protect residential privacy
              </label>
            </div>

            {/* Consent Notice */}
            <div style={{
              background: 'rgba(31, 41, 55, 0.5)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '10px 12px',
              display: 'flex',
              alignItems: 'flex-start',
              gap: 8,
            }}>
              <input
                type="checkbox"
                id="consentCheck"
                checked={consentGranted}
                onChange={(e) => setConsentGranted(e.target.checked)}
                style={{ marginTop: 3 }}
              />
              <label htmlFor="consentCheck" style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                I agree that this observation is publicly shared without personal identifiers to improve flood models and commuter safety.
              </label>
            </div>

            <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: 8 }}>
              <Send size={16} />
              <span>{loading ? 'Submitting...' : 'Submit Flood Observation'}</span>
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
