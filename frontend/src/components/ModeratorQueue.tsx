import React, { useState, useEffect } from 'react';
import { Check, X, ShieldAlert } from 'lucide-react';
import type { CommunityReport } from '../types';
import { fetchReports, reviewReport } from '../services/api';


interface ModeratorQueueProps {
  onReportUpdated: () => void;
}

export const ModeratorQueue: React.FC<ModeratorQueueProps> = ({ onReportUpdated }) => {
  const [reports, setReports] = useState<CommunityReport[]>([]);
  const [filter, setFilter] = useState<string>('UNVERIFIED');
  const [loading, setLoading] = useState(false);
  const [actionInProgress, setActionInProgress] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchReports(filter);
      setReports(data);
    } catch (err) {
      console.error('Failed to load reports:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [filter]);

  const handleReview = async (
    id: string,
    decision: 'VERIFIED' | 'REJECTED' | 'DUPLICATE',
    reason: string
  ) => {
    setActionInProgress(id);
    try {
      await reviewReport(id, decision, reason);
      await loadData();
      onReportUpdated();
    } catch (err) {
      console.error('Failed to review report:', err);
    } finally {
      setActionInProgress(null);
    }
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1000px', margin: '0 auto', overflowY: 'auto', height: '100%' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <div>
          <h2 style={{ fontSize: 20, fontWeight: 700 }}>Participatory Report Moderation Queue</h2>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 2 }}>
            Verify or reject ground-truth waterlogging observations submitted by citizens.
          </p>
        </div>

        {/* Filter buttons */}
        <div style={{ display: 'flex', gap: 6, background: 'var(--bg-surface-elevated)', padding: 4, borderRadius: 8 }}>
          {['UNVERIFIED', 'VERIFIED', 'REJECTED', 'ALL'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{
                background: filter === f ? '#06b6d4' : 'transparent',
                color: filter === f ? '#ffffff' : 'var(--text-secondary)',
                border: 'none',
                borderRadius: 6,
                padding: '6px 12px',
                fontSize: 12,
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              {f === 'UNVERIFIED' ? 'Pending (Queue)' : f}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Loading reports...</div>
      ) : reports.length === 0 ? (
        <div style={{
          textAlign: 'center',
          padding: '60px 20px',
          background: 'var(--bg-surface)',
          borderRadius: 12,
          border: '1px solid var(--border-subtle)',
        }}>
          <ShieldAlert size={36} color="#06b6d4" style={{ margin: '0 auto 12px' }} />
          <h4 style={{ fontSize: 16, fontWeight: 600 }}>No reports in this category</h4>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>
            All incoming flood submissions have been processed.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {reports.map((r) => (
            <div
              key={r.id}
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 10,
                padding: '16px 20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{
                    fontSize: 11,
                    fontWeight: 700,
                    padding: '2px 8px',
                    borderRadius: 4,
                    background: r.verification_status === 'VERIFIED' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                    color: r.verification_status === 'VERIFIED' ? '#10b981' : '#f59e0b',
                    border: `1px solid ${r.verification_status === 'VERIFIED' ? '#10b981' : '#f59e0b'}`,
                  }}>
                    {r.verification_status}
                  </span>
                  <span style={{ fontSize: 14, fontWeight: 700 }}>{r.category.replace(/_/g, ' ')}</span>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                    • {new Date(r.created_at).toLocaleTimeString()}
                  </span>
                </div>

                <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 6 }}>
                  Water Depth: <strong>{r.depth_range}</strong> | Passability: <strong>{r.road_passability.replace(/_/g, ' ')}</strong>
                </div>

                {r.notes && (
                  <div style={{ fontSize: 12, color: 'var(--text-primary)', marginTop: 6, fontStyle: 'italic' }}>
                    "{r.notes}"
                  </div>
                )}

                <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 6, fontFamily: 'var(--font-mono)' }}>
                  Location: {r.latitude.toFixed(4)}° N, {r.longitude.toFixed(4)}° E | ID: {r.id}
                </div>
              </div>

              {/* Review Buttons */}
              {r.verification_status === 'UNVERIFIED' && (
                <div style={{ display: 'flex', gap: 8 }}>
                  <button
                    className="btn-primary"
                    style={{ padding: '8px 14px', fontSize: 12, background: '#10b981' }}
                    disabled={actionInProgress === r.id}
                    onClick={() => handleReview(r.id, 'VERIFIED', 'Verified against traffic camera / municipal sensor')}
                  >
                    <Check size={14} />
                    <span>Verify</span>
                  </button>

                  <button
                    className="btn-secondary"
                    style={{ padding: '8px 14px', fontSize: 12, color: '#ef4444', borderColor: '#ef4444' }}
                    disabled={actionInProgress === r.id}
                    onClick={() => handleReview(r.id, 'REJECTED', 'False alarm or inaccurate depth estimate')}
                  >
                    <X size={14} />
                    <span>Reject</span>
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
