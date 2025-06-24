import React, { useEffect, useRef, useState } from 'react';
import Plotly from 'plotly.js/dist/plotly.min.js';
import { GraphConfig, AnalysisData } from '../App';
import { ParsedExpression, createMeshData } from '../utils/mathParser';

interface MathGrapherProps {
  config: GraphConfig;
  parsedExpression: ParsedExpression | null;
  analysisData: AnalysisData | null;
  error: string | null;
}

export const MathGrapher: React.FC<MathGrapherProps> = ({
  config,
  parsedExpression,
  analysisData,
  error
}) => {
  const plotRef = useRef<HTMLDivElement>(null);
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    if (!plotRef.current || !parsedExpression || !parsedExpression.isValid) {
      return;
    }

    const createPlot = async () => {
      try {
        // Generate mesh data
        const meshData = createMeshData(
          parsedExpression,
          config.xMin,
          config.xMax,
          config.yMin,
          config.yMax,
          config.resolution
        );

        const traces: any[] = [];

        // Main surface/plot trace
        if (config.graphType === 'surface') {
          traces.push({
            type: 'surface',
            x: meshData.x,
            y: meshData.y,
            z: meshData.z,
            colorscale: 'Greys',
            showscale: true,
            colorbar: {
              title: 'z',
              titlefont: { color: '#ffffff' },
              tickfont: { color: '#ffffff' },
              bgcolor: 'rgba(26, 26, 26, 0.8)',
              bordercolor: '#ffffff',
              len: 0.7
            },
            name: 'Surface',
            lighting: {
              ambient: 0.8,
              diffuse: 0.8,
              specular: 0.1,
              roughness: 0.1,
              fresnel: 0.2
            },
            contours: {
              z: {
                show: config.showGrid,
                color: '#666666',
                width: 1
              }
            }
          });
        } else if (config.graphType === 'wireframe') {
          traces.push({
            type: 'surface',
            x: meshData.x,
            y: meshData.y,
            z: meshData.z,
            colorscale: [[0, '#ffffff'], [1, '#ffffff']],
            showscale: false,
            surfacecolor: meshData.z.map(row => row.map(() => 0)),
            name: 'Wireframe',
            opacity: 1,
            contours: {
              x: { show: true, color: '#ffffff', width: 1 },
              y: { show: true, color: '#ffffff', width: 1 },
              z: { show: true, color: '#888888', width: 1 }
            }
          });
        } else if (config.graphType === 'contour') {
          traces.push({
            type: 'contour',
            x: meshData.x[0],
            y: meshData.y.map(row => row[0]),
            z: meshData.z,
            colorscale: 'Greys',
            showscale: true,
            colorbar: {
              title: 'z',
              titlefont: { color: '#ffffff' },
              tickfont: { color: '#ffffff' },
              bgcolor: 'rgba(26, 26, 26, 0.8)',
              bordercolor: '#ffffff'
            },
            line: { color: '#ffffff', width: 1 },
            name: 'Contour'
          });
        }

        // Add critical points if enabled
        if (config.showCriticalPoints && analysisData?.criticalPoints) {
          const criticalPoints = analysisData.criticalPoints;
          if (criticalPoints.length > 0) {
            const colors = {
              minimum: '#00ff00',
              maximum: '#ff0000',
              saddle: '#ffff00',
              unknown: '#ffffff'
            };

            criticalPoints.forEach((point, index) => {
              traces.push({
                type: 'scatter3d',
                x: [point.x],
                y: [point.y],
                z: [point.z],
                mode: 'markers',
                marker: {
                  size: 8,
                  color: colors[point.type],
                  symbol: 'diamond',
                  line: { color: '#000000', width: 2 }
                },
                name: `${point.type} (${point.x.toFixed(2)}, ${point.y.toFixed(2)})`,
                showlegend: true
              });
            });
          }
        }

        const layout = {
          paper_bgcolor: '#000000',
          plot_bgcolor: '#000000',
          font: { color: '#ffffff', family: 'Arial, sans-serif' },
          margin: { l: 0, r: 0, t: 0, b: 0 },
          scene: {
            bgcolor: '#000000',
            xaxis: {
              backgroundcolor: '#000000',
              gridcolor: '#333333',
              showbackground: true,
              zerolinecolor: '#666666',
              color: '#ffffff',
              title: { text: 'x', font: { color: '#ffffff' } }
            },
            yaxis: {
              backgroundcolor: '#000000',
              gridcolor: '#333333',
              showbackground: true,
              zerolinecolor: '#666666',
              color: '#ffffff',
              title: { text: 'y', font: { color: '#ffffff' } }
            },
            zaxis: {
              backgroundcolor: '#000000',
              gridcolor: '#333333',
              showbackground: true,
              zerolinecolor: '#666666',
              color: '#ffffff',
              title: { text: 'z', font: { color: '#ffffff' } }
            },
            camera: {
              eye: { x: 1.5, y: 1.5, z: 1.5 }
            }
          },
          showlegend: config.showCriticalPoints && analysisData?.criticalPoints?.length > 0,
          legend: {
            font: { color: '#ffffff' },
            bgcolor: 'rgba(0, 0, 0, 0.8)',
            bordercolor: '#ffffff',
            borderwidth: 1
          }
        };

        const plotConfig = {
          displayModeBar: true,
          modeBarButtonsToRemove: ['pan2d', 'select2d', 'lasso2d', 'autoScale2d'],
          modeBarButtonsToAdd: ['hoverClosestCartesian', 'toggleSpikelines'],
          displaylogo: false,
          responsive: true,
          scrollZoom: true
        };

        if (!isInitialized) {
          await Plotly.newPlot(plotRef.current, traces, layout, plotConfig);
          setIsInitialized(true);
        } else {
          await Plotly.react(plotRef.current, traces, layout, plotConfig);
        }

        // Make the plot extremely zoomable
        plotRef.current.on('plotly_relayout', (eventData: any) => {
          // Enable unlimited zooming
          if (eventData['scene.camera']) {
            // Allow very close zoom
            const camera = eventData['scene.camera'];
            if (camera.eye) {
              // Remove zoom limits
              delete camera.eye.x_range;
              delete camera.eye.y_range;
              delete camera.eye.z_range;
            }
          }
        });

      } catch (error) {
        console.error('Plot creation error:', error);
      }
    };

    createPlot();
  }, [config, parsedExpression, analysisData, isInitialized]);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (plotRef.current && isInitialized) {
        Plotly.Plots.resize(plotRef.current);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isInitialized]);

  return (
    <div 
      ref={plotRef} 
      style={{ 
        width: '100%', 
        height: '100%',
        background: '#000000'
      }}
    />
  );
};