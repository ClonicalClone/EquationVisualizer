import React, { useState } from 'react';
import { GraphConfig } from '../App';

interface FloatingControlsProps {
  config: GraphConfig;
  onConfigChange: (updates: Partial<GraphConfig>) => void;
  onEquationChange: (equation: string) => void;
  onToggleAnalysis: () => void;
  onToggleExamples: () => void;
  error: string | null;
}

export const FloatingControls: React.FC<FloatingControlsProps> = ({
  config,
  onConfigChange,
  onEquationChange,
  onToggleAnalysis,
  onToggleExamples,
  error
}) => {
  const [isMinimized, setIsMinimized] = useState(false);

  const handleEquationSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Equation is updated in real-time via onChange
  };

  return (
    <div 
      className="floating-card" 
      style={{ 
        top: '20px', 
        left: '20px',
        width: isMinimized ? '60px' : '320px',
        transition: 'width 0.3s ease'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h3 style={{ margin: 0 }}>{isMinimized ? '🔧' : '🔧 Controls'}</h3>
        <button 
          className="close-btn"
          onClick={() => setIsMinimized(!isMinimized)}
          style={{ position: 'relative', top: 0, right: 0 }}
        >
          {isMinimized ? '▶' : '◀'}
        </button>
      </div>

      {!isMinimized && (
        <>
          <form onSubmit={handleEquationSubmit}>
            <div className="input-group">
              <label>Mathematical Expression</label>
              <input
                type="text"
                value={config.equation}
                onChange={(e) => onEquationChange(e.target.value)}
                placeholder="e.g., x^2 + y^2, sin(x)*cos(y)"
                style={{ fontFamily: 'monospace' }}
              />
              {error && <div className="error-message">{error}</div>}
            </div>
          </form>

          <div className="input-group">
            <label>Graph Type</label>
            <select
              value={config.graphType}
              onChange={(e) => onConfigChange({ graphType: e.target.value as any })}
            >
              <option value="surface">3D Surface</option>
              <option value="wireframe">Wireframe</option>
              <option value="contour">Contour Plot</option>
              <option value="parametric">Parametric</option>
            </select>
          </div>

          <h4>Domain</h4>
          <div className="range-inputs">
            <div className="input-group">
              <label>X Min</label>
              <input
                type="number"
                value={config.xMin}
                onChange={(e) => onConfigChange({ xMin: parseFloat(e.target.value) })}
                step="0.5"
              />
            </div>
            <div className="input-group">
              <label>X Max</label>
              <input
                type="number"
                value={config.xMax}
                onChange={(e) => onConfigChange({ xMax: parseFloat(e.target.value) })}
                step="0.5"
              />
            </div>
            <div className="input-group">
              <label>Y Min</label>
              <input
                type="number"
                value={config.yMin}
                onChange={(e) => onConfigChange({ yMin: parseFloat(e.target.value) })}
                step="0.5"
              />
            </div>
            <div className="input-group">
              <label>Y Max</label>
              <input
                type="number"
                value={config.yMax}
                onChange={(e) => onConfigChange({ yMax: parseFloat(e.target.value) })}
                step="0.5"
              />
            </div>
          </div>

          <div className="input-group">
            <label>Resolution: {config.resolution}</label>
            <input
              type="range"
              min="20"
              max="200"
              value={config.resolution}
              onChange={(e) => onConfigChange({ resolution: parseInt(e.target.value) })}
              style={{
                width: '100%',
                height: '4px',
                background: 'rgba(255, 255, 255, 0.2)',
                outline: 'none',
                borderRadius: '2px'
              }}
            />
          </div>

          <h4>Display Options</h4>
          <div className="checkbox-group">
            <div className="checkbox-item">
              <input
                type="checkbox"
                id="criticalPoints"
                checked={config.showCriticalPoints}
                onChange={(e) => onConfigChange({ showCriticalPoints: e.target.checked })}
              />
              <label htmlFor="criticalPoints">Show Critical Points</label>
            </div>
            <div className="checkbox-item">
              <input
                type="checkbox"
                id="derivatives"
                checked={config.showDerivatives}
                onChange={(e) => onConfigChange({ showDerivatives: e.target.checked })}
              />
              <label htmlFor="derivatives">Show Derivatives</label>
            </div>
            <div className="checkbox-item">
              <input
                type="checkbox"
                id="grid"
                checked={config.showGrid}
                onChange={(e) => onConfigChange({ showGrid: e.target.checked })}
              />
              <label htmlFor="grid">Show Grid</label>
            </div>
          </div>

          <div className="btn-group">
            <button className="btn" onClick={onToggleAnalysis}>
              📊 Analysis
            </button>
            <button className="btn" onClick={onToggleExamples}>
              📚 Examples
            </button>
          </div>
        </>
      )}
    </div>
  );
};