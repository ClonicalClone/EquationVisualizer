import numpy as np
import sympy as sp
from sympy import symbols, diff, solve, limit, oo, Interval, solveset, S
from sympy.calculus.util import continuous_domain, function_range
import warnings
warnings.filterwarnings('ignore')

class AnalysisEngine:
    """
    Advanced mathematical analysis engine for calculus operations
    """
    
    def __init__(self):
        self.x, self.y, self.z, self.t = symbols('x y z t', real=True)
    
    def find_critical_points(self, expression, domain_x=(-10, 10), domain_y=(-10, 10)):
        """
        Find critical points of a multivariable function
        
        Args:
            expression (sympy.Expr): Function expression
            domain_x, domain_y (tuple): Search domain
            
        Returns:
            list: List of critical point coordinates (x, y, z)
        """
        critical_points = []
        
        try:
            # Calculate partial derivatives
            if self.x in expression.free_symbols and self.y in expression.free_symbols:
                fx = diff(expression, self.x)
                fy = diff(expression, self.y)
                
                # Solve system of equations fx = 0, fy = 0
                critical_system = [fx, fy]
                solutions = solve(critical_system, [self.x, self.y], dict=True)
                
                for sol in solutions:
                    try:
                        x_val = complex(sol.get(self.x, 0)).real
                        y_val = complex(sol.get(self.y, 0)).real
                        
                        # Check if solution is in domain
                        if (domain_x[0] <= x_val <= domain_x[1] and 
                            domain_y[0] <= y_val <= domain_y[1]):
                            
                            # Calculate z value
                            z_val = complex(expression.subs(sol)).real
                            
                            if np.isfinite(x_val) and np.isfinite(y_val) and np.isfinite(z_val):
                                critical_points.append((x_val, y_val, z_val))
                    
                    except (TypeError, ValueError):
                        continue
            
            elif self.x in expression.free_symbols:
                # Single variable case
                fx = diff(expression, self.x)
                solutions = solve(fx, self.x)
                
                for sol in solutions:
                    try:
                        x_val = complex(sol).real
                        if domain_x[0] <= x_val <= domain_x[1]:
                            y_val = complex(expression.subs(self.x, sol)).real
                            if np.isfinite(x_val) and np.isfinite(y_val):
                                critical_points.append((x_val, 0, y_val))
                    except (TypeError, ValueError):
                        continue
        
        except Exception as e:
            print(f"Critical points calculation error: {e}")
        
        return critical_points[:10]  # Limit to 10 points
    
    def calculate_derivatives(self, expression):
        """
        Calculate various derivatives of the expression
        
        Args:
            expression (sympy.Expr): Function expression
            
        Returns:
            dict: Dictionary containing derivative information
        """
        derivatives = {}
        
        try:
            # First partial derivatives
            if self.x in expression.free_symbols:
                derivatives['fx'] = diff(expression, self.x)
            if self.y in expression.free_symbols:
                derivatives['fy'] = diff(expression, self.y)
            
            # Second partial derivatives (Hessian components)
            if self.x in expression.free_symbols and self.y in expression.free_symbols:
                derivatives['fxx'] = diff(expression, self.x, 2)
                derivatives['fyy'] = diff(expression, self.y, 2)
                derivatives['fxy'] = diff(expression, self.x, self.y)
                
                # Calculate discriminant for critical point classification
                fxx = derivatives['fxx']
                fyy = derivatives['fyy']
                fxy = derivatives['fxy']
                derivatives['discriminant'] = fxx * fyy - fxy**2
            
            # Gradient magnitude
            if 'fx' in derivatives and 'fy' in derivatives:
                derivatives['gradient_magnitude'] = sp.sqrt(
                    derivatives['fx']**2 + derivatives['fy']**2
                )
            
        except Exception as e:
            print(f"Derivatives calculation error: {e}")
        
        return derivatives
    
    def calculate_limits(self, expression):
        """
        Calculate limits at boundaries and special points
        
        Args:
            expression (sympy.Expr): Function expression
            
        Returns:
            dict: Limit values at various points
        """
        limits_data = {}
        
        try:
            # Limits as x approaches infinity
            if self.x in expression.free_symbols:
                limits_data['x_to_inf'] = str(limit(expression, self.x, oo))
                limits_data['x_to_neg_inf'] = str(limit(expression, self.x, -oo))
            
            # Limits as y approaches infinity
            if self.y in expression.free_symbols:
                limits_data['y_to_inf'] = str(limit(expression, self.y, oo))
                limits_data['y_to_neg_inf'] = str(limit(expression, self.y, -oo))
            
            # Limit at origin
            if self.x in expression.free_symbols and self.y in expression.free_symbols:
                try:
                    # Approach origin along different paths
                    limit_along_x = limit(limit(expression, self.y, 0), self.x, 0)
                    limit_along_y = limit(limit(expression, self.x, 0), self.y, 0)
                    
                    limits_data['origin_via_x_axis'] = str(limit_along_x)
                    limits_data['origin_via_y_axis'] = str(limit_along_y)
                    
                    # Check if limits are equal (continuity indicator)
                    if limit_along_x == limit_along_y:
                        limits_data['origin_limit'] = str(limit_along_x)
                    else:
                        limits_data['origin_limit'] = "Does not exist"
                
                except Exception:
                    limits_data['origin_limit'] = "Cannot determine"
        
        except Exception as e:
            print(f"Limits calculation error: {e}")
        
        return limits_data
    
    def find_extrema(self, expression, x_min, x_max, y_min, y_max):
        """
        Find local and global extrema within a domain
        
        Args:
            expression (sympy.Expr): Function expression
            x_min, x_max, y_min, y_max (float): Domain boundaries
            
        Returns:
            dict: Extrema information
        """
        extrema = {
            'local_maxima': [],
            'local_minima': [],
            'saddle_points': [],
            'global_maximum': None,
            'global_minimum': None
        }
        
        try:
            # Find critical points
            critical_points = self.find_critical_points(expression, (x_min, x_max), (y_min, y_max))
            
            if not critical_points:
                return extrema
            
            # Calculate second derivatives for classification
            derivatives = self.calculate_derivatives(expression)
            
            if 'discriminant' in derivatives:
                fxx = derivatives['fxx']
                discriminant = derivatives['discriminant']
                
                for point in critical_points:
                    x_val, y_val, z_val = point
                    
                    # Evaluate discriminant at critical point
                    D_val = discriminant.subs([(self.x, x_val), (self.y, y_val)])
                    fxx_val = fxx.subs([(self.x, x_val), (self.y, y_val)])
                    
                    try:
                        D_numeric = complex(D_val).real
                        fxx_numeric = complex(fxx_val).real
                        
                        if D_numeric > 0:
                            if fxx_numeric > 0:
                                extrema['local_minima'].append(point)
                            else:
                                extrema['local_maxima'].append(point)
                        elif D_numeric < 0:
                            extrema['saddle_points'].append(point)
                        # D = 0 is inconclusive
                    
                    except (TypeError, ValueError):
                        continue
            
            # Find global extrema
            all_z_values = [point[2] for point in critical_points]
            if all_z_values:
                max_z = max(all_z_values)
                min_z = min(all_z_values)
                
                for point in critical_points:
                    if abs(point[2] - max_z) < 1e-10:
                        extrema['global_maximum'] = point
                    if abs(point[2] - min_z) < 1e-10:
                        extrema['global_minimum'] = point
        
        except Exception as e:
            print(f"Extrema calculation error: {e}")
        
        return extrema
    
    def analyze_function_properties(self, expression):
        """
        Analyze general properties of the function
        
        Args:
            expression (sympy.Expr): Function expression
            
        Returns:
            dict: Function properties
        """
        properties = {}
        
        try:
            # Variables in the expression
            free_vars = list(expression.free_symbols)
            properties['variables'] = [str(var) for var in free_vars]
            properties['dimension'] = len(free_vars)
            
            # Function type classification
            if expression.is_polynomial():
                properties['type'] = 'Polynomial'
                if len(free_vars) == 1:
                    properties['degree'] = sp.degree(expression, free_vars[0])
            elif expression.has(sp.sin, sp.cos, sp.tan):
                properties['type'] = 'Trigonometric'
            elif expression.has(sp.exp):
                properties['type'] = 'Exponential'
            elif expression.has(sp.log):
                properties['type'] = 'Logarithmic'
            else:
                properties['type'] = 'General'
            
            # Symmetry properties
            if len(free_vars) >= 1:
                var = free_vars[0]
                if expression.subs(var, -var) == expression:
                    properties['symmetry'] = 'Even function'
                elif expression.subs(var, -var) == -expression:
                    properties['symmetry'] = 'Odd function'
                else:
                    properties['symmetry'] = 'Neither even nor odd'
            
            # Periodicity check (basic)
            if expression.has(sp.sin, sp.cos):
                properties['periodic'] = 'Likely periodic (contains trig functions)'
            else:
                properties['periodic'] = 'Not obviously periodic'
            
            # Continuity analysis
            properties['continuous'] = 'Continuous everywhere' if not expression.has(1/self.x, 1/self.y) else 'May have discontinuities'
            
        except Exception as e:
            print(f"Properties analysis error: {e}")
            properties['error'] = str(e)
        
        return properties
    
    def analyze_surface_properties(self, expression):
        """
        Analyze properties specific to 3D surfaces
        
        Args:
            expression (sympy.Expr): Surface expression z = f(x,y)
            
        Returns:
            dict: Surface properties
        """
        surface_props = {}
        
        try:
            # Calculate derivatives for surface analysis
            derivatives = self.calculate_derivatives(expression)
            
            # Surface orientation and curvature information
            if 'fx' in derivatives and 'fy' in derivatives:
                fx, fy = derivatives['fx'], derivatives['fy']
                
                # Normal vector components (up to scaling)
                surface_props['normal_vector'] = f"(-{fx}, -{fy}, 1)"
                
                # Surface area element
                surface_props['area_element'] = f"sqrt(1 + ({fx})^2 + ({fy})^2)"
            
            # Curvature information
            if all(key in derivatives for key in ['fxx', 'fyy', 'fxy']):
                fxx, fyy, fxy = derivatives['fxx'], derivatives['fyy'], derivatives['fxy']
                
                # Mean curvature
                H = (fxx + fyy) / 2
                surface_props['mean_curvature'] = str(H)
                
                # Gaussian curvature
                K = fxx * fyy - fxy**2
                surface_props['gaussian_curvature'] = str(K)
            
            # Level curves information
            surface_props['level_curves'] = f"Curves where {expression} = constant"
            
        except Exception as e:
            print(f"Surface analysis error: {e}")
            surface_props['error'] = str(e)
        
        return surface_props
    
    def generate_comprehensive_report(self, expression):
        """
        Generate a comprehensive analysis report
        
        Args:
            expression (sympy.Expr): Function expression
            
        Returns:
            str: Formatted analysis report
        """
        report_lines = []
        report_lines.append("COMPREHENSIVE FUNCTION ANALYSIS REPORT")
        report_lines.append("=" * 50)
        
        # Basic information
        report_lines.append(f"\nFunction: f(x,y) = {expression}")
        
        # Properties
        properties = self.analyze_function_properties(expression)
        report_lines.append(f"\nFunction Type: {properties.get('type', 'Unknown')}")
        report_lines.append(f"Variables: {', '.join(properties.get('variables', []))}")
        report_lines.append(f"Dimension: {properties.get('dimension', 'Unknown')}")
        
        # Derivatives
        derivatives = self.calculate_derivatives(expression)
        if 'fx' in derivatives:
            report_lines.append(f"\n∂f/∂x = {derivatives['fx']}")
        if 'fy' in derivatives:
            report_lines.append(f"∂f/∂y = {derivatives['fy']}")
        
        # Critical points
        critical_points = self.find_critical_points(expression)
        if critical_points:
            report_lines.append(f"\nCritical Points: {len(critical_points)} found")
            for i, point in enumerate(critical_points[:5]):
                report_lines.append(f"  Point {i+1}: ({point[0]:.4f}, {point[1]:.4f}, {point[2]:.4f})")
        else:
            report_lines.append("\nNo critical points found in the analyzed domain.")
        
        # Limits
        limits = self.calculate_limits(expression)
        if limits:
            report_lines.append("\nLimit Analysis:")
            for direction, value in limits.items():
                report_lines.append(f"  {direction}: {value}")
        
        # Additional properties
        if 'symmetry' in properties:
            report_lines.append(f"\nSymmetry: {properties['symmetry']}")
        
        if 'continuous' in properties:
            report_lines.append(f"Continuity: {properties['continuous']}")
        
        return "\n".join(report_lines)
