import React, { useEffect, useRef, useState } from 'react';
import * as maplibregl from 'maplibre-gl';
import type { GeoJSONSource } from 'maplibre-gl';
import { Layers, Eye, EyeOff } from 'lucide-react';
import { fetchMapFeatures } from '../services/api';

interface InteractiveMapProps {
  onLocationSelect: (lat: number, lon: number, nameHint?: string) => void;
  selectedCoords?: { lat: number; lon: number } | null;
  refreshTrigger?: number;
}

export const InteractiveMap: React.FC<InteractiveMapProps> = ({
  onLocationSelect,
  selectedCoords,
  refreshTrigger,
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const markerRef = useRef<maplibregl.Marker | null>(null);


  const [layersVisibility, setLayersVisibility] = useState({
    susceptibility: true,
    roads: true,
    reports: true,
    observations: false,
  });

  const [mapLoaded, setMapLoaded] = useState(false);

  // Initialize MapLibre
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,

      style: {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: [
              'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
              'https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
            ],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors, CartoDB',
          },
        },
        layers: [
          {
            id: 'osm-tiles',
            type: 'raster',
            source: 'osm',
            minzoom: 0,
            maxzoom: 19,
          },
        ],
      },
      center: [72.8777, 19.0760], // Mumbai Center
      zoom: 11.2,
      maxBounds: [
        [72.60, 18.75], // SW
        [73.20, 19.45], // NE
      ],
    });

    map.addControl(new maplibregl.NavigationControl({ showCompass: true }), 'top-right');

    map.on('load', async () => {
      setMapLoaded(true);

      // 1. Susceptibility Source & Layers
      try {
        const gridGeoJSON = await fetchMapFeatures('susceptibility');
        map.addSource('susceptibility-source', {
          type: 'geojson',
          data: gridGeoJSON,
        });

        map.addLayer({
          id: 'susceptibility-fill',
          type: 'fill',
          source: 'susceptibility-source',
          paint: {
            'fill-color': ['get', 'color'],
            'fill-opacity': 0.40,
          },
        });

        map.addLayer({
          id: 'susceptibility-line',
          type: 'line',
          source: 'susceptibility-source',
          paint: {
            'line-color': ['get', 'color'],
            'line-width': 1,
            'line-opacity': 0.7,
          },
        });
      } catch (err) {
        console.error('Failed to load susceptibility layer:', err);
      }

      // 2. Critical Roads & Subways
      try {
        const roadsGeoJSON = await fetchMapFeatures('roads');
        map.addSource('roads-source', {
          type: 'geojson',
          data: roadsGeoJSON,
        });

        map.addLayer({
          id: 'roads-line',
          type: 'line',
          source: 'roads-source',
          paint: {
            'line-color': [
              'match',
              ['get', 'historical_vulnerability'],
              'CRITICAL', '#ef4444',
              'HIGH', '#f97316',
              'MODERATE', '#f59e0b',
              '#3b82f6',
            ],
            'line-width': [
              'case',
              ['get', 'is_subway'], 6,
              3.5,
            ],
          },
        });
      } catch (err) {
        console.error('Failed to load roads layer:', err);
      }

      // 3. Community Reports
      try {
        const reportsGeoJSON = await fetchMapFeatures('reports');
        map.addSource('reports-source', {
          type: 'geojson',
          data: reportsGeoJSON,
        });

        map.addLayer({
          id: 'reports-circle',
          type: 'circle',
          source: 'reports-source',
          paint: {
            'circle-color': [
              'match',
              ['get', 'verification_status'],
              'VERIFIED', '#06b6d4',
              '#f59e0b',
            ],
            'circle-radius': 7,
            'circle-stroke-width': 2,
            'circle-stroke-color': '#ffffff',
          },
        });
      } catch (err) {
        console.error('Failed to load reports layer:', err);
      }

      // 4. Historical Observations
      try {
        const obsGeoJSON = await fetchMapFeatures('observations');
        map.addSource('observations-source', {
          type: 'geojson',
          data: obsGeoJSON,
        });

        map.addLayer({
          id: 'observations-circle',
          type: 'circle',
          source: 'observations-source',
          layout: { visibility: 'none' },
          paint: {
            'circle-color': '#a855f7',
            'circle-radius': 6,
            'circle-stroke-width': 2,
            'circle-stroke-color': '#ffffff',
          },
        });
      } catch (err) {
        console.error('Failed to load observations layer:', err);
      }
    });

    // Map click handler to inspect location
    map.on('click', (e) => {
      const { lat, lng } = e.lngLat;
      onLocationSelect(lat, lng);
    });

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Update selected marker position
  useEffect(() => {
    if (!mapRef.current || !selectedCoords) return;

    if (!markerRef.current) {
      const el = document.createElement('div');
      el.className = 'custom-map-pin';
      el.style.width = '24px';
      el.style.height = '24px';
      el.style.backgroundColor = '#06b6d4';
      el.style.border = '3px solid white';
      el.style.borderRadius = '50%';
      el.style.boxShadow = '0 0 16px rgba(6, 182, 212, 0.9)';

      markerRef.current = new maplibregl.Marker({ element: el })
        .setLngLat([selectedCoords.lon, selectedCoords.lat])
        .addTo(mapRef.current);
    } else {
      markerRef.current.setLngLat([selectedCoords.lon, selectedCoords.lat]);
    }
  }, [selectedCoords]);

  // Refresh reports layer when trigger changes
  useEffect(() => {
    if (!mapRef.current || !mapLoaded) return;
    fetchMapFeatures('reports').then((data) => {
      const source = mapRef.current?.getSource('reports-source') as GeoJSONSource | undefined;
      if (source) {
        source.setData(data);
      }
    }).catch(console.error);
  }, [refreshTrigger, mapLoaded]);

  // Layer visibility toggles
  const toggleLayer = (layerKey: keyof typeof layersVisibility) => {
    if (!mapRef.current) return;
    const nextState = !layersVisibility[layerKey];
    setLayersVisibility((prev) => ({ ...prev, [layerKey]: nextState }));

    const visibilityVal = nextState ? 'visible' : 'none';

    if (layerKey === 'susceptibility') {
      mapRef.current.setLayoutProperty('susceptibility-fill', 'visibility', visibilityVal);
      mapRef.current.setLayoutProperty('susceptibility-line', 'visibility', visibilityVal);
    } else if (layerKey === 'roads') {
      mapRef.current.setLayoutProperty('roads-line', 'visibility', visibilityVal);
    } else if (layerKey === 'reports') {
      mapRef.current.setLayoutProperty('reports-circle', 'visibility', visibilityVal);
    } else if (layerKey === 'observations') {
      mapRef.current.setLayoutProperty('observations-circle', 'visibility', visibilityVal);
    }
  };

  return (
    <div className="map-canvas-container">
      <div ref={mapContainer} className="maplibre-viewport" />

      {/* Floating Layer Controller */}
      <div className="map-layer-controller">
        <div className="layer-control-title">
          <span>Map Intelligence Layers</span>
          <Layers size={14} />
        </div>

        <div className="layer-item" onClick={() => toggleLayer('susceptibility')}>
          <span>Static Susceptibility</span>
          {layersVisibility.susceptibility ? <Eye size={15} color="#06b6d4" /> : <EyeOff size={15} color="#6b7280" />}
        </div>

        <div className="layer-item" onClick={() => toggleLayer('roads')}>
          <span>Critical Roads & Subways</span>
          {layersVisibility.roads ? <Eye size={15} color="#06b6d4" /> : <EyeOff size={15} color="#6b7280" />}
        </div>

        <div className="layer-item" onClick={() => toggleLayer('reports')}>
          <span>Community Reports</span>
          {layersVisibility.reports ? <Eye size={15} color="#06b6d4" /> : <EyeOff size={15} color="#6b7280" />}
        </div>

        <div className="layer-item" onClick={() => toggleLayer('observations')}>
          <span>Historical Flood Hotspots</span>
          {layersVisibility.observations ? <Eye size={15} color="#06b6d4" /> : <EyeOff size={15} color="#6b7280" />}
        </div>

        <div className="layer-item disabled" title="Awaiting Copernicus Data Space connection">
          <span style={{ color: 'var(--text-muted)' }}>Sentinel-1 SAR Radar</span>
          <span style={{ fontSize: 10, background: '#374151', padding: '1px 5px', borderRadius: 4 }}>Pending</span>
        </div>
      </div>

      {/* Standardized Triple-Encoded Risk Legend */}
      <div className="map-legend">
        <div className="legend-title">Flood Risk Legend (Calibrated)</div>
        <div className="legend-row">
          <div className="legend-chip">
            <span className="legend-dot" style={{ backgroundColor: '#10b981' }} />
            <span>● Low (&lt;25%)</span>
          </div>
          <div className="legend-chip">
            <span className="legend-dot" style={{ backgroundColor: '#f59e0b' }} />
            <span>◆ Moderate</span>
          </div>
          <div className="legend-chip">
            <span className="legend-dot" style={{ backgroundColor: '#f97316' }} />
            <span>▲ High</span>
          </div>
          <div className="legend-chip">
            <span className="legend-dot" style={{ backgroundColor: '#ef4444' }} />
            <span>🛑 Critical (&gt;78%)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
