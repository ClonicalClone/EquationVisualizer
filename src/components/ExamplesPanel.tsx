import React from 'react';

interface ExamplesPanelProps {
  onSelectExample: (equation: string) => void;
  onClose: () => void;
}

const EXAMPLE_EQUATIONS = [
  {
    name: 'Paraboloid',
    equation: 'x^2 + y^2',
    description: 'Classic bowl shape'
  },
  {
    name: 'Saddle Point',
    equation: 'x^2 - y^2',
    description: 'Hyperbolic paraboloid'
  },
  {
    name: 'Gaussian Bell',
    equation: 'exp(-(x^2 + y^2))',
    description: '3D normal distribution'
  },
  {
    name: 'Sine Wave',
    equation: 'sin(x) * cos(y)',
    description: 'Trigonometric surface'
  },
  {
    name: 'Ripple Effect',
    equation: 'sin(sqrt(x^2 + y^2))',
    description: 'Circular wave pattern'
  },
  {
    name: 'Monkey Saddle',
    equation: 'x^3 - 3*x*y^2',
    description: 'Three-way saddle point'
  },
  {
    name: 'Hyperbolic',
    equation: 'x * y',
    description: 'Simple hyperbolic surface'
  },
  {
    name: 'Cone',
    equation: 'sqrt(x^2 + y^2)',
    description: 'Circular cone'
  },
  {
    name: 'Mexican Hat',
    equation: '(1 - x^2 - y^2) * exp(-(x^2 + y^2)/2)',
    description: 'Sombrero function'
  },
  {
    name: 'Egg Crate',
    equation: 'sin(x) * sin(y)',
    description: 'Periodic bumps pattern'
  },
  {
    name: 'Twisted Surface',
    equation: 'x*y + x^3 - y^3',
    description: 'Complex twisted topology'
  },
  {
    name: 'Logarithmic',
    equation: 'log(x^2 + y^2 + 1)',
    description: 'Logarithmic growth'
  },
  {
    name: 'Absolute Valley',
    equation: 'abs(x) + abs(y)',
    description: 'Pyramid with sharp edges'
  },
  {
    name: 'Peaks Function',
    equation: '3*(1-x)^2*exp(-(x^2) - (y+1)^2) - 10*(x/5 - x^3 - y^5)*exp(-x^2-y^2) - 1/3*exp(-(x+1)^2 - y^2)',
    description: 'Multiple peaks and valleys'
  },
  {
    name: 'Rosenbrock',
    equation: '(1-x)^2 + 100*(y-x^2)^2',
    description: 'Optimization test function'
  }
];

export const ExamplesPanel: React.FC<ExamplesPanelProps> = ({
  onSelectExample,
  onClose
}) => {
  return (
    <div 
      className="floating-card" 
      style={{ 
        bottom: '20px', 
        left: '20px',
        width: '400px',
        maxHeight: '60vh'
      }}
    >
      <h3>📚 Example Equations</h3>
      <button className="close-btn" onClick={onClose}>×</button>
      
      <div className="scrollable">
        <div className="examples-grid">
          {EXAMPLE_EQUATIONS.map((example, index) => (
            <div 
              key={index}
              className="example-item"
              onClick={() => onSelectExample(example.equation)}
            >
              <div className="example-name">{example.name}</div>
              <div className="example-equation">{example.equation}</div>
              <div style={{ 
                fontSize: '11px', 
                color: '#999999', 
                marginTop: '4px',
                fontStyle: 'italic'
              }}>
                {example.description}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};