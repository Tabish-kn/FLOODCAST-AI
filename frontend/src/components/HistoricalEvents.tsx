import React, { useState, useEffect } from 'react';
import { CloudRain, Calendar, MapPin, Info } from 'lucide-react';
import type { FloodEvent } from '../types';
import { fetchFloodEvents } from '../services/api';


interface HistoricalEventsProps {
  onSelectHotspot: (lat: number, lon: number) => void;
}

export const HistoricalEvents: React.FC<HistoricalEventsProps> = ({ onSelectHotspot }) => {
  const [events, setEvents] = useState<FloodEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchFloodEvents()
      .then((data) => {
        setEvents(data);
        if (data.length > 0) setSelectedEventId(data[0].id);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const activeEvent = events.find((e) => e.id === selectedEventId);

  return (
    <div style={{ padding: '24px', maxWidth: '1000px', margin: '0 auto', overflowY: 'auto', height: '100%' }}>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 20, fontWeight: 700 }}>Mumbai Historical Deluge Archive</h2>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 2 }}>
          Ground-truth recorded waterlogging events used for spatial and event-based model validation.
        </p>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Loading event archive...</div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: 20 }}>
          {/* Left Event List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {events.map((e) => {
              const isSelected = e.id === selectedEventId;
              return (
                <div
                  key={e.id}
                  onClick={() => setSelectedEventId(e.id)}
                  style={{
                    background: isSelected ? 'rgba(6, 182, 212, 0.12)' : 'var(--bg-surface)',
                    border: `1px solid ${isSelected ? 'var(--accent-cyan)' : 'var(--border-subtle)'}`,
                    borderRadius: 10,
                    padding: '14px 16px',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, color: '#38bdf8', fontWeight: 600 }}>
                    <Calendar size={12} />
                    <span>{e.event_date}</span>
                  </div>
                  <div style={{ fontSize: 15, fontWeight: 700, marginTop: 4, color: isSelected ? '#38bdf8' : 'var(--text-primary)' }}>
                    {e.name}
                  </div>
                  <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 6, display: 'flex', gap: 12 }}>
                    <span>Rain: <strong>{e.total_rainfall_mm} mm</strong></span>
                    <span>Peak: <strong>{e.peak_intensity_mm_h} mm/h</strong></span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right Event Detail */}
          {activeEvent && (
            <div style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 12,
              padding: '24px',
              display: 'flex',
              flexDirection: 'column',
              gap: 18,
            }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <CloudRain size={24} color="#06b6d4" />
                  <h3 style={{ fontSize: 18, fontWeight: 700 }}>{activeEvent.name}</h3>
                </div>
                <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 6, lineHeight: 1.5 }}>
                  {activeEvent.description}
                </div>
              </div>

              {/* Rain metrics */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <div className="metric-card">
                  <div className="metric-label">Total 24h Rainfall</div>
                  <div className="metric-value">{activeEvent.total_rainfall_mm} mm</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Peak Hourly Intensity</div>
                  <div className="metric-value">{activeEvent.peak_intensity_mm_h} mm/h</div>
                </div>
              </div>

              {/* Recorded Observations */}
              <div>
                <h4 style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, textTransform: 'uppercase', color: 'var(--text-secondary)' }}>
                  Documented Inundation Hotspots ({activeEvent.observations?.length || 0})
                </h4>

                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {activeEvent.observations?.map((o) => (
                    <div
                      key={o.id}
                      style={{
                        background: 'var(--bg-surface-elevated)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: 8,
                        padding: '12px 16px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                      }}
                    >
                      <div>
                        <div style={{ fontSize: 14, fontWeight: 600 }}>{o.location_name}</div>
                        <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 2 }}>
                          Depth: <strong>{o.water_depth_cm} cm</strong> | Source: {o.observation_source}
                        </div>
                      </div>
                      <button
                        className="btn-secondary"
                        style={{ padding: '6px 12px', fontSize: 12 }}
                        onClick={() => onSelectHotspot(o.latitude, o.longitude)}
                      >
                        <MapPin size={13} color="#06b6d4" />
                        <span>Inspect Risk</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              <div className="limitations-box">
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontWeight: 600, color: 'var(--text-primary)' }}>
                  <Info size={14} color="#06b6d4" />
                  <span>Research &amp; Benchmark Note</span>
                </div>
                <div style={{ marginTop: 4 }}>
                  This historical event is part of the held-out validation suite. Models are strictly tested on these independent observations to ensure geographic and temporal generalization without spatial leakage.
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
