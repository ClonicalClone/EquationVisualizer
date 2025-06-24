import { evaluate, parse, MathNode } from 'mathjs';

export interface ParsedExpression {
  node: MathNode;
  variables: string[];
  isValid: boolean;
  errorMessage?: string;
}

export function parseMathExpression(equation: string): ParsedExpression {
  try {
    // Clean the equation string
    let cleanEquation = equation.trim();
    
    // Handle equation format (z = f(x,y) or f(x,y))
    if (cleanEquation.includes('=')) {
      const parts = cleanEquation.split('=');
      if (parts.length === 2) {
        const left = parts[0].trim();
        const right = parts[1].trim();
        if (left === 'z' || left === 'y' || left === 'f') {
          cleanEquation = right;
        } else {
          // Assume implicit equation, move to one side
          cleanEquation = `(${left}) - (${right})`;
        }
      }
    }
    
    // Replace common mathematical notation
    cleanEquation = cleanEquation
      .replace(/\^/g, '^')  // Power
      .replace(/×/g, '*')   // Multiplication
      .replace(/÷/g, '/')   // Division
      .replace(/−/g, '-')   // Minus
      .replace(/π/g, 'pi')  // Pi
      .replace(/sin⁻¹/g, 'asin')
      .replace(/cos⁻¹/g, 'acos')
      .replace(/tan⁻¹/g, 'atan')
      .replace(/ln/g, 'log')
      .replace(/√/g, 'sqrt');
    
    // Handle implicit multiplication
    cleanEquation = cleanEquation
      .replace(/(\d)([a-zA-Z])/g, '$1*$2')  // 2x -> 2*x
      .replace(/([a-zA-Z])(\d)/g, '$1*$2')  // x2 -> x*2
      .replace(/\)([a-zA-Z(])/g, ')*$1')    // )(x -> )*(x
      .replace(/([a-zA-Z])\(/g, '$1*(');    // x( -> x*(
    
    // Parse the expression
    const node = parse(cleanEquation);
    
    // Extract variables
    const variables = extractVariables(node);
    
    return {
      node,
      variables,
      isValid: true
    };
    
  } catch (error) {
    return {
      node: parse('0'), // fallback
      variables: [],
      isValid: false,
      errorMessage: error instanceof Error ? error.message : 'Unknown parsing error'
    };
  }
}

function extractVariables(node: MathNode): string[] {
  const variables = new Set<string>();
  
  node.traverse((node, path, parent) => {
    if (node.type === 'SymbolNode') {
      const name = (node as any).name;
      // Only include single-letter variables and common math variables
      if (/^[a-zA-Z]$/.test(name) || ['pi', 'e'].includes(name)) {
        if (!['pi', 'e', 'sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'abs', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh'].includes(name)) {
          variables.add(name);
        }
      }
    }
  });
  
  return Array.from(variables).sort();
}

export function evaluateExpression(
  parsedExpr: ParsedExpression, 
  variables: Record<string, number>
): number {
  try {
    if (!parsedExpr.isValid) {
      return NaN;
    }
    
    const result = parsedExpr.node.evaluate(variables);
    return typeof result === 'number' ? result : NaN;
  } catch (error) {
    return NaN;
  }
}

export function createMeshData(
  parsedExpr: ParsedExpression,
  xMin: number,
  xMax: number,
  yMin: number,
  yMax: number,
  resolution: number
): { x: number[][], y: number[][], z: number[][] } {
  const x: number[][] = [];
  const y: number[][] = [];
  const z: number[][] = [];
  
  const xStep = (xMax - xMin) / (resolution - 1);
  const yStep = (yMax - yMin) / (resolution - 1);
  
  for (let i = 0; i < resolution; i++) {
    x[i] = [];
    y[i] = [];
    z[i] = [];
    
    for (let j = 0; j < resolution; j++) {
      const xVal = xMin + j * xStep;
      const yVal = yMin + i * yStep;
      
      x[i][j] = xVal;
      y[i][j] = yVal;
      
      const zVal = evaluateExpression(parsedExpr, { x: xVal, y: yVal });
      z[i][j] = isFinite(zVal) ? zVal : null;
    }
  }
  
  return { x, y, z };
}