import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sympy as sp
from sympy import symbols, diff, limit, solve, oo, simplify, lambdify
import warnings
warnings.filterwarnings('ignore')

from math_parser import MathParser
from graph_generator import GraphGenerator
from analysis_engine import AnalysisEngine

# Page configuration
st.set_page_config(
    page_title="3D Mathematical Grapher",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for black and white theme
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #1a1a1a;
    }
    .stTextInput > div > div > input {
        background-color: #2a2a2a;
        color: #ffffff;
        border-color: #ffffff;
    }
    .stSelectbox > div > div > select {
        background-color: #2a2a2a;
        color: #ffffff;
        border-color: #ffffff;
    }
    .stSlider > div > div > div {
        color: #ffffff;
    }
    .stMarkdown {
        color: #ffffff;
    }
    .stAlert {
        background-color: #2a2a2a;
        color: #ffffff;
        border-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🔬 3D Mathematical Grapher")
    st.markdown("**Comprehensive equation visualization with calculus analysis**")
    
    # Initialize components
    parser = MathParser()
    generator = GraphGenerator()
    analyzer = AnalysisEngine()
    
    # Sidebar controls
    with st.sidebar:
        st.header("📊 Graph Controls")
        
        # Equation input
        equation = st.text_input(
            "Enter Equation",
            value="x**2 + y**2",
            help="Examples: x**2 + y**2, sin(x)*cos(y), x**3 - 3*x*y**2"
        )
        
        # Graph type selection
        graph_type = st.selectbox(
            "Graph Type",
            ["3D Surface", "2D Function", "Parametric 3D", "Contour Plot"]
        )
        
        # Domain settings
        st.subheader("Domain Settings")
        col1, col2 = st.columns(2)
        with col1:
            x_min = st.number_input("X Min", value=-5.0, step=0.5)
            y_min = st.number_input("Y Min", value=-5.0, step=0.5)
        with col2:
            x_max = st.number_input("X Max", value=5.0, step=0.5)
            y_max = st.number_input("Y Max", value=5.0, step=0.5)
        
        # Resolution
        resolution = st.slider("Resolution", min_value=20, max_value=200, value=50)
        
        # Analysis options
        st.subheader("Analysis Options")
        show_derivatives = st.checkbox("Show Derivatives", value=True)
        show_critical_points = st.checkbox("Show Critical Points", value=True)
        show_limits = st.checkbox("Show Limits", value=False)
        show_asymptotes = st.checkbox("Show Asymptotes", value=False)
        
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            # Parse equation
            parsed_expr = parser.parse_equation(equation)
            
            if parsed_expr is not None:
                # Generate graph based on type
                if graph_type == "3D Surface":
                    fig = generator.create_3d_surface(
                        parsed_expr, x_min, x_max, y_min, y_max, resolution
                    )
                elif graph_type == "2D Function":
                    # Convert to 2D by setting y=0 or treating as single variable
                    fig = generator.create_2d_plot(
                        parsed_expr, x_min, x_max, resolution
                    )
                elif graph_type == "Parametric 3D":
                    fig = generator.create_parametric_3d(
                        parsed_expr, x_min, x_max, y_min, y_max, resolution
                    )
                elif graph_type == "Contour Plot":
                    fig = generator.create_contour_plot(
                        parsed_expr, x_min, x_max, y_min, y_max, resolution
                    )
                
                # Add analysis overlays
                if show_critical_points:
                    critical_points = analyzer.find_critical_points(parsed_expr)
                    fig = generator.add_critical_points(fig, critical_points)
                
                if show_derivatives and graph_type == "3D Surface":
                    derivative_data = analyzer.calculate_derivatives(parsed_expr)
                    fig = generator.add_derivative_visualization(fig, derivative_data)
                
                # Display the graph
                st.plotly_chart(fig, use_container_width=True, theme=None)
                
            else:
                st.error("Invalid equation format. Please check your syntax.")
                
        except Exception as e:
            st.error(f"Error generating graph: {str(e)}")
            st.info("Try a simpler equation or check the syntax.")
    
    with col2:
        st.subheader("📈 Analysis Results")
        
        try:
            if 'parsed_expr' in locals() and parsed_expr is not None:
                # Display equation information
                st.write("**Original Equation:**")
                st.latex(f"z = {sp.latex(parsed_expr)}")
                
                # Calculate and display derivatives
                if show_derivatives:
                    st.write("**Partial Derivatives:**")
                    x, y = symbols('x y')
                    
                    if x in parsed_expr.free_symbols:
                        dx = diff(parsed_expr, x)
                        st.latex(f"\\frac{{\\partial z}}{{\\partial x}} = {sp.latex(dx)}")
                    
                    if y in parsed_expr.free_symbols:
                        dy = diff(parsed_expr, y)
                        st.latex(f"\\frac{{\\partial z}}{{\\partial y}} = {sp.latex(dy)}")
                
                # Critical points analysis
                if show_critical_points:
                    st.write("**Critical Points:**")
                    critical_points = analyzer.find_critical_points(parsed_expr)
                    if critical_points:
                        for i, point in enumerate(critical_points[:5]):  # Limit to 5 points
                            st.write(f"Point {i+1}: ({point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f})")
                    else:
                        st.write("No critical points found in the domain.")
                
                # Function properties
                st.write("**Function Properties:**")
                properties = analyzer.analyze_function_properties(parsed_expr)
                for prop, value in properties.items():
                    st.write(f"• {prop}: {value}")
                
                # Limits analysis
                if show_limits:
                    st.write("**Limit Analysis:**")
                    limits_data = analyzer.calculate_limits(parsed_expr)
                    for direction, limit_val in limits_data.items():
                        st.write(f"• {direction}: {limit_val}")
                
        except Exception as e:
            st.write(f"Analysis error: {str(e)}")
    
    # Additional features section
    st.markdown("---")
    st.subheader("🔧 Advanced Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generate Function Report"):
            if 'parsed_expr' in locals() and parsed_expr is not None:
                report = analyzer.generate_comprehensive_report(parsed_expr)
                st.text_area("Comprehensive Analysis Report", report, height=200)
    
    with col2:
        if st.button("🎯 Find Extrema"):
            if 'parsed_expr' in locals() and parsed_expr is not None:
                extrema = analyzer.find_extrema(parsed_expr, x_min, x_max, y_min, y_max)
                st.json(extrema)
    
    with col3:
        if st.button("📐 Surface Analysis"):
            if 'parsed_expr' in locals() and parsed_expr is not None:
                surface_props = analyzer.analyze_surface_properties(parsed_expr)
                st.json(surface_props)
    
    # Example equations
    with st.expander("📚 Example Equations"):
        examples = {
            "Paraboloid": "x**2 + y**2",
            "Saddle Point": "x**2 - y**2",
            "Gaussian": "exp(-(x**2 + y**2))",
            "Sine Wave": "sin(x) * cos(y)",
            "Ripple": "sin(sqrt(x**2 + y**2))",
            "Monkey Saddle": "x**3 - 3*x*y**2",
            "Hyperbolic": "x*y",
            "Cone": "sqrt(x**2 + y**2)"
        }
        
        for name, eq in examples.items():
            if st.button(f"{name}: {eq}"):
                st.rerun()

if __name__ == "__main__":
    main()
