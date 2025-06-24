import { useState, useCallback, useEffect } from 'react';
import { MathGrapher } from './components/MathGrapher';
import { FloatingControls } from './components/FloatingControls';
import { AnalysisPanel } from './components/AnalysisPanel';
import { ExamplesPanel } from './components/ExamplesPanel';
import { parseMathExpression } from './utils/mathParser';
import { analyzeExpression } from './utils/mathAnalysis';
import './App.css';

export interface GraphConfig {
  equation: string;
  xMin: number;
  xMax: number;
  yMin: number;
  yMax: number;
  resolution: number;
  graphType: 'surface' | 'contour' | 'parametric' | 'wireframe';
  showCriticalPoints: boolean;
  showDerivatives: boolean;
  showGrid: boolean;
}

export interface AnalysisData {
  derivatives: any;
  criticalPoints: Array<{x: number, y: number, z: number, type: string}>;
  limits: any;
  properties: any;
}

function App() {
  const [config, setConfig] = useState<GraphConfig>({
    equation: 'x^2 + y^2',
    xMin: -5,
    xMax: 5,
    yMin: -5,
    yMax: 5,
    resolution: 50,
    graphType: 'surface',
    showCriticalPoints: true,
    showDerivatives: false,
    showGrid: true
  });

  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [showExamples, setShowExamples] = useState(false);
  const [parsedExpression, setParsedExpression] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const updateConfig = useCallback((updates: Partial<GraphConfig>) => {
    setConfig(prev => ({ ...prev, ...updates }));
  }, []);

  const handleEquationChange = useCallback((equation: string) => {
    setError(null);
    try {
      const parsed = parseMathExpression(equation);
      setParsedExpression(parsed);
      updateConfig({ equation });
      
      // Perform analysis
      const analysis = analyzeExpression(parsed, config.xMin, config.xMax, config.yMin, config.yMax);
      setAnalysisData(analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid equation');
      setParsedExpression(null);
      setAnalysisData(null);
    }
  }, [config.xMin, config.xMax, config.yMin, config.yMax, updateConfig]);

  const handleExampleSelect = useCallback((equation: string) => {
    handleEquationChange(equation);
    setShowExamples(false);
  }, [handleEquationChange]);

  // Initialize with default equation
  useEffect(() => {
    handleEquationChange(config.equation);
  }, []);

  return (
    <div className="app">
      <MathGrapher 
        config={config}
        parsedExpression={parsedExpression}
        analysisData={analysisData}
        error={error}
      />
      
      <FloatingControls
        config={config}
        onConfigChange={updateConfig}
        onEquationChange={handleEquationChange}
        onToggleAnalysis={() => setShowAnalysis(!showAnalysis)}
        onToggleExamples={() => setShowExamples(!showExamples)}
        error={error}
      />

      {showAnalysis && analysisData && (
        <AnalysisPanel
          analysisData={analysisData}
          equation={config.equation}
          onClose={() => setShowAnalysis(false)}
        />
      )}

      {showExamples && (
        <ExamplesPanel
          onSelectExample={handleExampleSelect}
          onClose={() => setShowExamples(false)}
        />
      )}
    </div>
  );
}

export default App;