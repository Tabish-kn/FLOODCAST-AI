import React from 'react';
import { Info, Database, AlertCircle } from 'lucide-react';


export const AboutView: React.FC = () => {
  return (
    <div style={{ padding: '28px', maxWidth: '900px', margin: '0 auto', overflowY: 'auto', height: '100%', lineHeight: 1.6 }}>
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 22, fontWeight: 700 }}>About FloodCast AI</h2>
        <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginTop: 4 }}>
          A climate-risk research and hyperlocal decision-support platform for urban flood intelligence in Mumbai, India.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        {/* Four Distinct Capabilities Section */}
        <div style={{
          background: 'var(--bg-surface)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 12,
          padding: '24px',
        }}>
          <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
            <Info size={18} color="#06b6d4" />
            <span>Four Distinct Analytical Capabilities</span>
          </h3>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 16 }}>
            A core principle of FloodCast AI is that <strong>a static susceptibility map or historical footprint is never represented as a live forecast</strong>:
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
            <div style={{ background: 'var(--bg-surface-elevated)', padding: 14, borderRadius: 8 }}>
              <div style={{ fontWeight: 700, fontSize: 13, color: '#38bdf8' }}>1. Static Flood Susceptibility</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 4 }}>
                Physical baseline vulnerability determined by topographic elevation, slope, terrain concavity, and distance to tidal choke points.
              </div>
            </div>

            <div style={{ background: 'var(--bg-surface-elevated)', padding: 14, borderRadius: 8 }}>
              <div style={{ fontWeight: 700, fontSize: 13, color: '#a855f7' }}>2. Historical Observations</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 4 }}>
                Documented ground-truth waterlogging records from municipal disaster logs (July 2005, August 2017, July 2021, July 2023).
              </div>
            </div>

            <div style={{ background: 'var(--bg-surface-elevated)', padding: 14, borderRadius: 8 }}>
              <div style={{ fontWeight: 700, fontSize: 13, color: '#f59e0b' }}>3. Participatory Reporting</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 4 }}>
                Near real-time citizen and fleet driver reports with transparent verification status (Verified vs. Pending moderation).
              </div>
            </div>

            <div style={{ background: 'var(--bg-surface-elevated)', padding: 14, borderRadius: 8 }}>
              <div style={{ fontWeight: 700, fontSize: 13, color: '#10b981' }}>4. Short-Horizon Forecasting</div>
              <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 4 }}>
                1-6 hour predictive hazard conditioned on incoming radar precipitation nowcasts and antecedent soil saturation.
              </div>
            </div>
          </div>
        </div>

        {/* Data Sources & Coordinate System */}
        <div style={{
          background: 'var(--bg-surface)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 12,
          padding: '24px',
        }}>
          <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
            <Database size={18} color="#06b6d4" />
            <span>Study Area &amp; Geospatial Data Sources</span>
          </h3>

          <div style={{ fontSize: 13, color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div>
              <strong>Study Area:</strong> Mumbai Metropolitan Region (Bounds: Longitude 72.75°–73.05° E, Latitude 18.85°–19.30° N).
            </div>
            <div>
              <strong>Coordinate Reference System:</strong> WGS 84 (<code>EPSG:4326</code>) for APIs/GeoJSON interchange; UTM Zone 43N (<code>EPSG:32643</code>) for metric distance and slope calculations.
            </div>
            <div>
              <strong>Elevation &amp; Slope:</strong> Calibrated against high-resolution NASA SRTM 30m and municipal survey benchmarks.
            </div>
            <div>
              <strong>Infrastructure:</strong> OpenStreetMap road network and railway line corridors with specialized underpass tags.
            </div>
          </div>
        </div>

        {/* Safety Disclaimer */}
        <div style={{
          background: 'rgba(245, 158, 11, 0.1)',
          border: '1px solid rgba(245, 158, 11, 0.3)',
          borderRadius: 12,
          padding: '20px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontWeight: 700, color: '#f59e0b', fontSize: 14 }}>
            <AlertCircle size={18} />
            <span>Important Operational Disclaimer</span>
          </div>
          <div style={{ fontSize: 13, color: 'var(--text-primary)', marginTop: 8 }}>
            FloodCast AI is an informational decision-support and research platform. A low flood risk score on a road segment does not guarantee safe vehicular passage; physical debris, displaced manhole covers, or electric utility hazards may exist. Always obey local emergency directives issued by the Municipal Corporation of Greater Mumbai (MCGM) and Mumbai Police.
          </div>
        </div>
      </div>
    </div>
  );
};
