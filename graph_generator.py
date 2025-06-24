import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sympy as sp
from sympy import lambdify, symbols
import warnings
warnings.filterwarnings('ignore')

class GraphGenerator:
    """
    Advanced graph generation for mathematical functions with black/white aesthetics
    """
    
    def __init__(self):
        self.x, self.y = symbols('x y')
        self.color_scheme = {
            'background': '#000000',
            'surface': '#ffffff',
            'critical_points': '#ff0000',
            'derivatives': '#00ff00',
            'grid': '#333333',
            'text': '#ffffff'
        }
        
        self.layout_template = dict(
            paper_bgcolor='#000000',
            plot_bgcolor='#000000',
            font=dict(color='#ffffff'),
            scene=dict(
                bgcolor='#000000',
                xaxis=dict(
                    backgroundcolor='#000000',
                    gridcolor='#333333',
                    showbackground=True,
                    zerolinecolor='#666666',
                    color='#ffffff'
                ),
                yaxis=dict(
                    backgroundcolor='#000000',
                    gridcolor='#333333',
                    showbackground=True,
                    zerolinecolor='#666666',
                    color='#ffffff'
                ),
                zaxis=dict(
                    backgroundcolor='#000000',
                    gridcolor='#333333',
                    showbackground=True,
                    zerolinecolor='#666666',
                    color='#ffffff'
                )
            )
        )
    
    def create_3d_surface(self, expression, x_min, x_max, y_min, y_max, resolution):
        """
        Create 3D surface plot from mathematical expression
        
        Args:
            expression (sympy.Expr): Parsed mathematical expression
            x_min, x_max, y_min, y_max (float): Domain boundaries
            resolution (int): Grid resolution
            
        Returns:
            plotly.graph_objects.Figure: 3D surface plot
        """
        # Create coordinate grids
        x_vals = np.linspace(x_min, x_max, resolution)
        y_vals = np.linspace(y_min, y_max, resolution)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        # Convert expression to numerical function
        try:
            func = lambdify([self.x, self.y], expression, 'numpy')
            Z = func(X, Y)
            
            # Handle complex results by taking real part
            if np.iscomplexobj(Z):
                Z = np.real(Z)
            
            # Replace infinities and NaNs
            Z = np.where(np.isfinite(Z), Z, np.nan)
            
        except Exception as e:
            print(f"Function evaluation error: {e}")
            Z = np.zeros_like(X)
        
        # Create 3D surface
        fig = go.Figure()
        
        # Add surface with white/gray colorscale
        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Greys',
            showscale=True,
            colorbar=dict(
                title="z",
                titlefont=dict(color='#ffffff'),
                tickfont=dict(color='#ffffff'),
                bgcolor='#1a1a1a',
                bordercolor='#ffffff'
            ),
            name='Surface'
        ))
        
        # Update layout with black theme
        fig.update_layout(
            title=dict(
                text=f'3D Surface: z = {str(expression)}',
                font=dict(color='#ffffff', size=16)
            ),
            **self.layout_template
        )
        
        return fig
    
    def create_2d_plot(self, expression, x_min, x_max, resolution):
        """
        Create 2D plot for single-variable functions
        
        Args:
            expression (sympy.Expr): Mathematical expression
            x_min, x_max (float): Domain boundaries
            resolution (int): Number of points
            
        Returns:
            plotly.graph_objects.Figure: 2D plot
        """
        x_vals = np.linspace(x_min, x_max, resolution * 2)
        
        try:
            # Handle both single and multi-variable expressions
            if self.y in expression.free_symbols:
                # Set y=0 for visualization or create a surface projection
                expr_2d = expression.subs(self.y, 0)
            else:
                expr_2d = expression
            
            func = lambdify(self.x, expr_2d, 'numpy')
            y_vals = func(x_vals)
            
            # Handle complex results
            if np.iscomplexobj(y_vals):
                y_vals = np.real(y_vals)
            
            # Replace infinities
            y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
            
        except Exception as e:
            print(f"2D function evaluation error: {e}")
            y_vals = np.zeros_like(x_vals)
        
        fig = go.Figure()
        
        # Add main function line
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode='lines',
            line=dict(color='#ffffff', width=2),
            name=f'y = {str(expr_2d)}'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f'2D Plot: y = {str(expr_2d)}',
                font=dict(color='#ffffff', size=16)
            ),
            paper_bgcolor='#000000',
            plot_bgcolor='#000000',
            font=dict(color='#ffffff'),
            xaxis=dict(
                gridcolor='#333333',
                zerolinecolor='#666666',
                color='#ffffff'
            ),
            yaxis=dict(
                gridcolor='#333333',
                zerolinecolor='#666666',
                color='#ffffff'
            )
        )
        
        return fig
    
    def create_parametric_3d(self, expression, x_min, x_max, y_min, y_max, resolution):
        """
        Create parametric 3D plot
        """
        # For parametric plots, we'll create a curve in 3D space
        t_vals = np.linspace(0, 2*np.pi, resolution)
        
        try:
            # Create parametric equations
            x_param = t_vals
            y_param = np.sin(t_vals)
            
            # Use the expression for z-coordinate
            func = lambdify([self.x, self.y], expression, 'numpy')
            z_param = func(x_param, y_param)
            
            if np.iscomplexobj(z_param):
                z_param = np.real(z_param)
            
        except Exception:
            x_param = t_vals
            y_param = np.sin(t_vals)
            z_param = np.cos(t_vals)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter3d(
            x=x_param, y=y_param, z=z_param,
            mode='lines+markers',
            line=dict(color='#ffffff', width=4),
            marker=dict(color='#ffffff', size=3),
            name='Parametric Curve'
        ))
        
        fig.update_layout(
            title=dict(
                text='Parametric 3D Curve',
                font=dict(color='#ffffff', size=16)
            ),
            **self.layout_template
        )
        
        return fig
    
    def create_contour_plot(self, expression, x_min, x_max, y_min, y_max, resolution):
        """
        Create contour plot
        """
        x_vals = np.linspace(x_min, x_max, resolution)
        y_vals = np.linspace(y_min, y_max, resolution)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        try:
            func = lambdify([self.x, self.y], expression, 'numpy')
            Z = func(X, Y)
            
            if np.iscomplexobj(Z):
                Z = np.real(Z)
            
            Z = np.where(np.isfinite(Z), Z, np.nan)
            
        except Exception:
            Z = X**2 + Y**2  # Fallback
        
        fig = go.Figure()
        
        fig.add_trace(go.Contour(
            x=x_vals, y=y_vals, z=Z,
            colorscale='Greys',
            showscale=True,
            colorbar=dict(
                title="z",
                titlefont=dict(color='#ffffff'),
                tickfont=dict(color='#ffffff'),
                bgcolor='#1a1a1a',
                bordercolor='#ffffff'
            ),
            line=dict(color='#ffffff', width=1)
        ))
        
        fig.update_layout(
            title=dict(
                text=f'Contour Plot: {str(expression)}',
                font=dict(color='#ffffff', size=16)
            ),
            paper_bgcolor='#000000',
            plot_bgcolor='#000000',
            font=dict(color='#ffffff'),
            xaxis=dict(
                gridcolor='#333333',
                zerolinecolor='#666666',
                color='#ffffff'
            ),
            yaxis=dict(
                gridcolor='#333333',
                zerolinecolor='#666666',
                color='#ffffff'
            )
        )
        
        return fig
    
    def add_critical_points(self, fig, critical_points):
        """
        Add critical points to existing figure
        
        Args:
            fig (plotly.graph_objects.Figure): Existing figure
            critical_points (list): List of critical point coordinates
            
        Returns:
            plotly.graph_objects.Figure: Figure with critical points added
        """
        if not critical_points:
            return fig
        
        # Extract coordinates
        x_coords = [point[0] for point in critical_points]
        y_coords = [point[1] for point in critical_points]
        z_coords = [point[2] for point in critical_points]
        
        # Add critical points as scatter3d
        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='markers',
            marker=dict(
                color='#ff0000',
                size=8,
                symbol='diamond'
            ),
            name='Critical Points'
        ))
        
        return fig
    
    def add_derivative_visualization(self, fig, derivative_data):
        """
        Add derivative visualization to figure
        """
        # This would add gradient field or directional derivatives
        # For now, we'll add a simple annotation
        fig.add_annotation(
            text="Derivatives calculated",
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False,
            font=dict(color='#00ff00', size=12),
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='#00ff00'
        )
        
        return fig
    
    def create_multiple_functions(self, expressions, x_min, x_max, y_min, y_max, resolution):
        """
        Create plot with multiple functions overlaid
        """
        fig = go.Figure()
        
        colors = ['#ffffff', '#cccccc', '#999999', '#666666']
        
        for i, expr in enumerate(expressions):
            try:
                x_vals = np.linspace(x_min, x_max, resolution)
                y_vals = np.linspace(y_min, y_max, resolution)
                X, Y = np.meshgrid(x_vals, y_vals)
                
                func = lambdify([self.x, self.y], expr, 'numpy')
                Z = func(X, Y)
                
                if np.iscomplexobj(Z):
                    Z = np.real(Z)
                
                Z = np.where(np.isfinite(Z), Z, np.nan)
                
                fig.add_trace(go.Surface(
                    x=X, y=Y, z=Z,
                    colorscale=[[0, colors[i % len(colors)]], [1, colors[i % len(colors)]]],
                    opacity=0.7,
                    name=f'Function {i+1}',
                    showscale=False
                ))
                
            except Exception as e:
                print(f"Error plotting function {i}: {e}")
                continue
        
        fig.update_layout(
            title=dict(
                text='Multiple Functions Overlay',
                font=dict(color='#ffffff', size=16)
            ),
            **self.layout_template
        )
        
        return fig
