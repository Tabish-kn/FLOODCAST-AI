import React, { useState, useEffect } from 'react';
import { Cpu, BarChart3, ShieldCheck, Layers } from 'lucide-react';

import { fetchModelMetrics } from '../services/api';

export const ModelEvaluationView: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchModelMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ padding: '24px', maxWidth: '1000px', margin: '0 auto', overflowY: 'auto', height: '100%' }}>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 20, fontWeight: 700 }}>ML Architecture &amp; Scientific Validation</h2>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 2 }}>
          Reproducible evaluation metrics, spatial holdouts, and feature importance for Mumbai flood models.
        </p>
      </div>

      {loading || !metrics ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Loading model evaluation...</div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {/* Active Model Header Card */}
          <div style={{
            background: 'var(--bg-surface)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 12,
            padding: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <div style={{
                width: 44,
                height: 44,
                borderRadius: 10,
                background: 'rgba(6, 182, 212, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#06b6d4',
              }}>
                <Cpu size={24} />
              </div>
              <div>
                <div style={{ fontSize: 16, fontWeight: 700 }}>{metrics.model_version || 'v1.0-rf-mumbai'}</div>
                <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 2 }}>
                  Algorithm: <strong>Calibrated Random Forest (Isotonic Regression)</strong> | Target: <strong>Static Susceptibility</strong>
                </div>
              </div>
            </div>
            <div style={{
              background: 'rgba(16, 185, 129, 0.15)',
              color: '#10b981',
              border: '1px solid #10b981',
              padding: '4px 12px',
              borderRadius: 20,
              fontSize: 12,
              fontWeight: 700,
            }}>
              ACTIVE INFERENCE
            </div>
          </div>

          {/* Validation Split Comparison Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            {/* Spatial Holdout Card */}
            <div style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 12,
              padding: '20px',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                <Layers size={18} color="#06b6d4" />
                <h4 style={{ fontSize: 15, fontWeight: 700 }}>1. Spatial Holdout (Island City)</h4>
              </div>
              <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 14 }}>
                Trained exclusively on Western &amp; Eastern Suburbs; tested on unseen Island City (South Mumbai). Prevents spatial autocorrelation leakage.
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div className="metric-card">
                  <div className="metric-label">PR-AUC</div>
                  <div className="metric-value">{metrics.spatial_holdout?.pr_auc}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Brier Score</div>
                  <div className="metric-value">{metrics.spatial_holdout?.brier_score}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Precision</div>
                  <div className="metric-value">{Math.round((metrics.spatial_holdout?.precision || 0) * 100)}%</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Test Samples</div>
                  <div className="metric-value">{metrics.spatial_holdout?.sample_size}</div>
                </div>
              </div>
            </div>

            {/* Event Holdout Card */}
            <div style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 12,
              padding: '20px',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                <BarChart3 size={18} color="#38bdf8" />
                <h4 style={{ fontSize: 15, fontWeight: 700 }}>2. Event Holdout (2023 Deluge)</h4>
              </div>
              <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 14 }}>
                Trained on events up to 2021; evaluated on the entire unseen July 2023 monsoon deluge season. Tests temporal transferability.
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div className="metric-card">
                  <div className="metric-label">PR-AUC</div>
                  <div className="metric-value">{metrics.event_holdout?.pr_auc}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Brier Score</div>
                  <div className="metric-value">{metrics.event_holdout?.brier_score}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Precision</div>
                  <div className="metric-value">{Math.round((metrics.event_holdout?.precision || 0) * 100)}%</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Test Samples</div>
                  <div className="metric-value">{metrics.event_holdout?.sample_size}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Feature Importances */}
          {metrics.feature_importances && (
            <div style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 12,
              padding: '20px',
            }}>
              <h4 style={{ fontSize: 15, fontWeight: 700, marginBottom: 14 }}>
                Hydrological Feature Importance Breakdown
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {Object.entries(metrics.feature_importances).map(([feature, weight]: [string, any]) => (
                  <div key={feature}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 4 }}>
                      <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                        {feature.replace(/_/g, ' ').toUpperCase()}
                      </span>
                      <span style={{ fontFamily: 'var(--font-mono)', color: '#38bdf8' }}>
                        {Math.round(weight * 100)}%
                      </span>
                    </div>
                    <div style={{ height: 6, background: 'var(--bg-primary)', borderRadius: 3, overflow: 'hidden' }}>
                      <div
                        style={{
                          height: '100%',
                          width: `${weight * 100}%`,
                          background: 'linear-gradient(90deg, #06b6d4, #3b82f6)',
                          borderRadius: 3,
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Scientific Integrity Rulebook Reminder */}
          <div className="limitations-box">
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontWeight: 700, color: 'var(--text-primary)' }}>
              <ShieldCheck size={16} color="#10b981" />
              <span>Scientific Integrity &amp; Calibration Guarantee</span>
            </div>
            <div style={{ marginTop: 6, lineHeight: 1.5 }}>
              In accordance with <code>RULES.md</code>, FloodCast AI uses calibrated probabilities fitted via Isotonic regression rather than uncalibrated raw ensemble votes. Missing reports are never treated as confirmed non-flood zones, and random pixel splits are rejected to prevent spatial data leakage.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
