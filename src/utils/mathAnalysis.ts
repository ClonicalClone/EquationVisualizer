import { derivative, parse } from 'mathjs';
import { ParsedExpression, evaluateExpression } from './mathParser';

export interface DerivativeData {
  fx?: string;
  fy?: string;
  fxx?: string;
  fyy?: string;
  fxy?: string;
}

export interface CriticalPoint {
  x: number;
  y: number;
  z: number;
  type: 'minimum' | 'maximum' | 'saddle' | 'unknown';
}

export interface LimitData {
  xToInf: string;
  xToNegInf: string;
  yToInf: string;
  yToNegInf: string;
  atOrigin: string;
}

export interface FunctionProperties {
  type: string;
  variables: string[];
  dimension: number;
  symmetry: string;
  continuity: string;
  domain: string;
}

export interface AnalysisResult {
  derivatives: DerivativeData;
  criticalPoints: CriticalPoint[];
  limits: LimitData;
  properties: FunctionProperties;
}

export function analyzeExpression(
  parsedExpr: ParsedExpression,
  xMin: number,
  xMax: number,
  yMin: number,
  yMax: number
): AnalysisResult {
  const derivatives = calculateDerivatives(parsedExpr);
  const criticalPoints = findCriticalPoints(parsedExpr, derivatives, xMin, xMax, yMin, yMax);
  const limits = calculateLimits(parsedExpr);
  const properties = analyzeProperties(parsedExpr);
  
  return {
    derivatives,
    criticalPoints,
    limits,
    properties
  };
}

function calculateDerivatives(parsedExpr: ParsedExpression): DerivativeData {
  const derivatives: DerivativeData = {};
  
  try {
    if (!parsedExpr.isValid) return derivatives;
    
    const variables = parsedExpr.variables;
    
    if (variables.includes('x')) {
      try {
        const fx = derivative(parsedExpr.node, 'x');
        derivatives.fx = fx.toString();
        
        // Second derivative with respect to x
        const fxx = derivative(fx, 'x');
        derivatives.fxx = fxx.toString();
        
        // Mixed partial if y is present
        if (variables.includes('y')) {
          const fxy = derivative(fx, 'y');
          derivatives.fxy = fxy.toString();
        }
      } catch (error) {
        console.warn('Error calculating x derivatives:', error);
      }
    }
    
    if (variables.includes('y')) {
      try {
        const fy = derivative(parsedExpr.node, 'y');
        derivatives.fy = fy.toString();
        
        // Second derivative with respect to y
        const fyy = derivative(fy, 'y');
        derivatives.fyy = fyy.toString();
      } catch (error) {
        console.warn('Error calculating y derivatives:', error);
      }
    }
  } catch (error) {
    console.warn('General derivative calculation error:', error);
  }
  
  return derivatives;
}

function findCriticalPoints(
  parsedExpr: ParsedExpression,
  derivatives: DerivativeData,
  xMin: number,
  xMax: number,
  yMin: number,
  yMax: number
): CriticalPoint[] {
  const criticalPoints: CriticalPoint[] = [];
  
  try {
    if (!parsedExpr.isValid || !derivatives.fx || !derivatives.fy) {
      return criticalPoints;
    }
    
    // For now, use numerical method to find critical points
    // This is a simplified approach - in a full implementation,
    // you'd want to use a proper numerical solver
    const step = 0.5;
    const tolerance = 0.1;
    
    for (let x = xMin; x <= xMax; x += step) {
      for (let y = yMin; y <= yMax; y += step) {
        try {
          const fxNode = parse(derivatives.fx);
          const fyNode = parse(derivatives.fy);
          
          const fxVal = fxNode.evaluate({ x, y });
          const fyVal = fyNode.evaluate({ x, y });
          
          // Check if both partial derivatives are close to zero
          if (Math.abs(fxVal) < tolerance && Math.abs(fyVal) < tolerance) {
            const z = evaluateExpression(parsedExpr, { x, y });
            
            if (isFinite(z)) {
              const type = classifyCriticalPoint(derivatives, x, y);
              criticalPoints.push({ x, y, z, type });
            }
          }
        } catch (error) {
          // Skip this point if evaluation fails
          continue;
        }
      }
    }
  } catch (error) {
    console.warn('Critical points calculation error:', error);
  }
  
  return criticalPoints.slice(0, 10); // Limit to 10 points
}

function classifyCriticalPoint(
  derivatives: DerivativeData,
  x: number,
  y: number
): 'minimum' | 'maximum' | 'saddle' | 'unknown' {
  try {
    if (!derivatives.fxx || !derivatives.fyy || !derivatives.fxy) {
      return 'unknown';
    }
    
    const fxxNode = parse(derivatives.fxx);
    const fyyNode = parse(derivatives.fyy);
    const fxyNode = parse(derivatives.fxy);
    
    const fxxVal = fxxNode.evaluate({ x, y });
    const fyyVal = fyyNode.evaluate({ x, y });
    const fxyVal = fxyNode.evaluate({ x, y });
    
    const discriminant = fxxVal * fyyVal - fxyVal * fxyVal;
    
    if (discriminant > 0) {
      return fxxVal > 0 ? 'minimum' : 'maximum';
    } else if (discriminant < 0) {
      return 'saddle';
    } else {
      return 'unknown';
    }
  } catch (error) {
    return 'unknown';
  }
}

function calculateLimits(_parsedExpr: ParsedExpression): LimitData {
  // Simplified limit analysis - in a full implementation,
  // you'd use more sophisticated limit calculation
  return {
    xToInf: 'Not calculated',
    xToNegInf: 'Not calculated',
    yToInf: 'Not calculated',
    yToNegInf: 'Not calculated',
    atOrigin: 'Not calculated'
  };
}

function analyzeProperties(parsedExpr: ParsedExpression): FunctionProperties {
  const variables = parsedExpr.variables;
  const exprString = parsedExpr.node.toString();
  
  // Basic type classification
  let type = 'General';
  if (exprString.includes('sin') || exprString.includes('cos') || exprString.includes('tan')) {
    type = 'Trigonometric';
  } else if (exprString.includes('exp')) {
    type = 'Exponential';
  } else if (exprString.includes('log')) {
    type = 'Logarithmic';
  } else if (/^[\d\s+\-*/^xy()]+$/.test(exprString.replace(/\s/g, ''))) {
    type = 'Polynomial';
  }
  
  // Basic symmetry check
  let symmetry = 'No obvious symmetry';
  try {
    if (variables.includes('x') && !variables.includes('y')) {
      // Test for even/odd function
      const testVal = evaluateExpression(parsedExpr, { x: 1 });
      const testNegVal = evaluateExpression(parsedExpr, { x: -1 });
      
      if (Math.abs(testVal - testNegVal) < 1e-10) {
        symmetry = 'Even function (f(-x) = f(x))';
      } else if (Math.abs(testVal + testNegVal) < 1e-10) {
        symmetry = 'Odd function (f(-x) = -f(x))';
      }
    }
  } catch (error) {
    // Skip symmetry analysis on error
  }
  
  return {
    type,
    variables,
    dimension: variables.length,
    symmetry,
    continuity: 'Continuous (assumed)',
    domain: 'Real numbers (assumed)'
  };
}