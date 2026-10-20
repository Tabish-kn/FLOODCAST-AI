import React, { useState, useEffect } from 'react';
import {
  Waves,
  Map as MapIcon,
  Clock,
  ShieldAlert,
  Cpu,
  Info,
  Plus,
  Radio,
} from 'lucide-react';
import { InteractiveMap } from './components/InteractiveMap';
import { RiskInspectorPanel } from './components/RiskInspectorPanel';
import { ReportModal } from './components/ReportModal';
import { ModeratorQueue } from './components/ModeratorQueue';
import { HistoricalEvents } from './components/HistoricalEvents';
import { ModelEvaluationView } from './components/ModelEvaluationView';
import { AboutView } from './components/AboutView';
import { queryRisk, fetchReports } from './services/api';
import type { PredictionResult } from './types';


type ActiveTab = 'map' | 'events' | 'moderation' | 'models' | 'about';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ActiveTab>('map');
  const [selectedCoords, setSelectedCoords] = useState<{ lat: number; lon: number } | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [inspectorLoading, setInspectorLoading] = useState(false);
  const [reportModalOpen, setReportModalOpen] = useState(false);
  const [reportCoords, setReportCoords] = useState<{ lat: number; lon: number } | null>(null);
  const [pendingReportsCount, setPendingReportsCount] = useState(0);
  const [refreshCounter, setRefreshCounter] = useState(0);

  // Load count of pending unverified reports for header badge
  const updatePendingCount = async () => {
    try {
      const reports = await fetchReports('UNVERIFIED');
      setPendingReportsCount(reports.length);
    } catch (e) {
      // Ignore initial background error
    }
  };

  useEffect(() => {
    updatePendingCount();
  }, [refreshCounter]);

  // Handle location selection from map click or hotspot click
  const handleLocationSelect = async (lat: number, lon: number) => {
    setSelectedCoords({ lat, lon });
    setInspectorLoading(true);
    try {
      const pred = await queryRisk(lat, lon);
      setPrediction(pred);
    } catch (err) {
      console.error('Failed to query risk:', err);
    } finally {
      setInspectorLoading(false);
    }
  };

  const handleOpenReportModal = (lat?: number, lon?: number) => {
    if (lat && lon) {
      setReportCoords({ lat, lon });
    } else if (selectedCoords) {
      setReportCoords(selectedCoords);
    } else {
      setReportCoords({ lat: 19.0760, lon: 72.8777 }); // Default Mumbai center
    }
    setReportModalOpen(true);
  };

  const handleHotspotSelectFromEvents = (lat: number, lon: number) => {
    setActiveTab('map');
    handleLocationSelect(lat, lon);
  };

  return (
    <div className="app-container">
      {/* Top Header */}
      <header className="app-header">
        <div className="brand-section">
          <div className="brand-logo-icon">
            <Waves size={20} />
          </div>
          <div>
            <div className="brand-title">FloodCast AI</div>
          </div>
          <div className="study-area-badge">
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#06b6d4' }} />
            <span>Mumbai MMR</span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="nav-tabs">
          <button
            className={`nav-tab-btn ${activeTab === 'map' ? 'active' : ''}`}
            onClick={() => setActiveTab('map')}
          >
            <MapIcon size={15} />
            <span>Risk Map</span>
          </button>

          <button
            className={`nav-tab-btn ${activeTab === 'events' ? 'active' : ''}`}
            onClick={() => setActiveTab('events')}
          >
            <Clock size={15} />
            <span>Historical Deluges</span>
          </button>

          <button
            className={`nav-tab-btn ${activeTab === 'moderation' ? 'active' : ''}`}
            onClick={() => setActiveTab('moderation')}
          >
            <ShieldAlert size={15} />
            <span>Moderation</span>
            {pendingReportsCount > 0 && (
              <span style={{
                background: '#f59e0b',
                color: '#111827',
                fontSize: 10,
                fontWeight: 700,
                padding: '1px 5px',
                borderRadius: 10,
              }}>
                {pendingReportsCount}
              </span>
            )}
          </button>

          <button
            className={`nav-tab-btn ${activeTab === 'models' ? 'active' : ''}`}
            onClick={() => setActiveTab('models')}
          >
            <Cpu size={15} />
            <span>Model Validation</span>
          </button>

          <button
            className={`nav-tab-btn ${activeTab === 'about' ? 'active' : ''}`}
            onClick={() => setActiveTab('about')}
          >
            <Info size={15} />
            <span>About</span>
          </button>
        </nav>

        {/* Freshness / Live Status Badge */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            fontSize: 11,
            color: '#38bdf8',
            background: 'rgba(6, 182, 212, 0.12)',
            padding: '4px 10px',
            borderRadius: 6,
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            fontWeight: 600,
          }}>
            <Radio size={12} color="#06b6d4" />
            <span>INFERENCE READY</span>
          </div>
        </div>
      </header>

      {/* Honest Mode Banner */}
      <div className="demo-banner">
        <span>
          ℹ️ <strong>ACTIVE MODE:</strong> Calibrated Baseline Susceptibility Model (v1.0-rf-mumbai) with synthetic demonstration telemetry.
        </span>
        <span style={{ opacity: 0.85 }}>
          Study Area Bounds: 18.85°N–19.30°N, 72.75°E–73.05°E
        </span>
      </div>

      {/* Main Body */}
      <main className="app-content">
        {activeTab === 'map' && (
          <>
            <InteractiveMap
              onLocationSelect={handleLocationSelect}
              selectedCoords={selectedCoords}
              refreshTrigger={refreshCounter}
            />

            {/* Location Risk Inspector Slide-out */}
            {prediction && (
              <RiskInspectorPanel
                prediction={prediction}
                loading={inspectorLoading}
                onClose={() => setPrediction(null)}
                onOpenReportModal={handleOpenReportModal}
              />
            )}

            {/* Quick Report FAB Button */}
            <button
              className="fab-report-btn"
              onClick={() => handleOpenReportModal()}
              title="Submit flood observation"
            >
              <Plus size={18} />
              <span>Report Flooding</span>
            </button>
          </>
        )}

        {activeTab === 'events' && (
          <HistoricalEvents onSelectHotspot={handleHotspotSelectFromEvents} />
        )}

        {activeTab === 'moderation' && (
          <ModeratorQueue onReportUpdated={() => setRefreshCounter((c) => c + 1)} />
        )}

        {activeTab === 'models' && <ModelEvaluationView />}

        {activeTab === 'about' && <AboutView />}
      </main>

      {/* Community Report Modal */}
      <ReportModal
        isOpen={reportModalOpen}
        onClose={() => setReportModalOpen(false)}
        defaultCoords={reportCoords}
        onReportSubmitted={() => setRefreshCounter((c) => c + 1)}
      />
    </div>
  );
};

export default App;
