import { } from 'react';
import { AnalysisData } from '../App';

interface AnalysisPanelProps {
  analysisData: AnalysisData;
  equation: string;
  onClose: () => void;
}

export const AnalysisPanel = ({
  analysisData,
  equation,
  onClose
}: any) => {
  return (
    <div 
      className="floating-card" 
      style={{ 
        top: '20px', 
        right: '20px',
        width: '350px',
        maxHeight: '80vh'
      }}
    >
      <h3>📊 Mathematical Analysis</h3>
      <button className="close-btn" onClick={onClose}>×</button>
      
      <div className="scrollable analysis-content">
        <div className="analysis-section">
          <h4>Function</h4>
          <div className="latex-display">
            z = {equation}
          </div>
        </div>

        {analysisData.derivatives && (
          <div className="analysis-section">
            <h4>Partial Derivatives</h4>
            {analysisData.derivatives.fx && (
              <div className="latex-display">
                ∂z/∂x = {analysisData.derivatives.fx}
              </div>
            )}
            {analysisData.derivatives.fy && (
              <div className="latex-display">
                ∂z/∂y = {analysisData.derivatives.fy}
              </div>
            )}
            {analysisData.derivatives.fxx && (
              <div className="latex-display">
                ∂²z/∂x² = {analysisData.derivatives.fxx}
              </div>
            )}
            {analysisData.derivatives.fyy && (
              <div className="latex-display">
                ∂²z/∂y² = {analysisData.derivatives.fyy}
              </div>
            )}
            {analysisData.derivatives.fxy && (
              <div className="latex-display">
                ∂²z/∂x∂y = {analysisData.derivatives.fxy}
              </div>
            )}
          </div>
        )}

        {analysisData.criticalPoints && analysisData.criticalPoints.length > 0 && (
          <div className="analysis-section">
            <h4>Critical Points ({analysisData.criticalPoints.length})</h4>
            {analysisData.criticalPoints.map((point, index) => (
              <div key={index} className="analysis-section">
                <p><strong>Point {index + 1}:</strong></p>
                <p>Coordinates: ({point.x.toFixed(4)}, {point.y.toFixed(4)}, {point.z.toFixed(4)})</p>
                <p>Type: <span style={{ 
                  color: point.type === 'minimum' ? '#00ff00' : 
                        point.type === 'maximum' ? '#ff0000' : 
                        point.type === 'saddle' ? '#ffff00' : '#ffffff'
                }}>{point.type}</span></p>
              </div>
            ))}
          </div>
        )}

        {analysisData.properties && (
          <div className="analysis-section">
            <h4>Function Properties</h4>
            <p><strong>Type:</strong> {analysisData.properties.type}</p>
            <p><strong>Variables:</strong> {analysisData.properties.variables.join(', ')}</p>
            <p><strong>Dimension:</strong> {analysisData.properties.dimension}D</p>
            <p><strong>Symmetry:</strong> {analysisData.properties.symmetry}</p>
            <p><strong>Continuity:</strong> {analysisData.properties.continuity}</p>
            <p><strong>Domain:</strong> {analysisData.properties.domain}</p>
          </div>
        )}

        {analysisData.limits && (
          <div className="analysis-section">
            <h4>Limit Behavior</h4>
            <p><strong>As x → ∞:</strong> {analysisData.limits.xToInf}</p>
            <p><strong>As x → -∞:</strong> {analysisData.limits.xToNegInf}</p>
            <p><strong>As y → ∞:</strong> {analysisData.limits.yToInf}</p>
            <p><strong>As y → -∞:</strong> {analysisData.limits.yToNegInf}</p>
            <p><strong>At origin:</strong> {analysisData.limits.atOrigin}</p>
          </div>
        )}
      </div>
    </div>
  );
};