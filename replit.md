# 3D Mathematical Grapher

## Overview

This is a Streamlit-based web application that provides advanced 3D mathematical graphing capabilities. The application allows users to input mathematical expressions and visualize them as interactive 3D plots with comprehensive analysis features including critical point detection, derivative visualization, and mathematical analysis.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit web interface with custom black/white theming
- **Backend**: Python-based mathematical processing using SymPy and NumPy
- **Visualization**: Plotly for interactive 3D graphics
- **Deployment**: Replit autoscale deployment with Streamlit server

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Primary Streamlit interface and application orchestration
- **Features**: Custom CSS theming, user input handling, component integration
- **Architecture Decision**: Chose Streamlit for rapid prototyping and built-in web server capabilities
- **Rationale**: Streamlit provides excellent mathematical visualization capabilities with minimal setup

### 2. Mathematical Parser (`math_parser.py`)
- **Purpose**: Converts string mathematical expressions into SymPy expressions
- **Features**: Support for various equation formats, function recognition, input validation
- **Architecture Decision**: Used SymPy as the core symbolic mathematics library
- **Rationale**: SymPy provides comprehensive symbolic math capabilities and seamless integration with NumPy

### 3. Graph Generator (`graph_generator.py`)
- **Purpose**: Creates interactive 3D visualizations using Plotly
- **Features**: Black/white color scheme, multiple plot types, customizable layouts
- **Architecture Decision**: Plotly chosen over matplotlib for 3D visualization
- **Rationale**: Plotly offers superior interactive 3D graphics and web-based rendering

### 4. Analysis Engine (`analysis_engine.py`)
- **Purpose**: Performs advanced mathematical analysis (critical points, derivatives, etc.)
- **Features**: Critical point detection, multivariable calculus operations
- **Architecture Decision**: Separate analysis module for complex mathematical operations
- **Rationale**: Modular design allows for easier testing and extension of mathematical features

## Data Flow

1. **User Input**: Mathematical expressions entered through Streamlit interface
2. **Parsing**: `MathParser` converts string input to SymPy expressions
3. **Analysis**: `AnalysisEngine` performs mathematical analysis on parsed expressions
4. **Visualization**: `GraphGenerator` creates 3D plots using Plotly
5. **Display**: Streamlit renders the interactive visualizations in the web interface

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **SymPy**: Symbolic mathematics library
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualization library

### Development Tools
- **Python 3.11**: Runtime environment
- **Nix**: Package management and reproducible builds
- **UV**: Fast Python package installer

## Deployment Strategy

- **Platform**: Replit autoscale deployment
- **Runtime**: Python 3.11 with Nix package management
- **Server**: Streamlit development server on port 5000
- **Scaling**: Autoscale deployment target for automatic resource management

### Configuration Decisions
- **Port 5000**: Standard port for development, configured in both .replit and Streamlit config
- **Headless Mode**: Server runs without GUI for deployment environments
- **Address Binding**: 0.0.0.0 for external access in containerized environments

## Changelog

```
Changelog:
- June 24, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```

## Technical Notes

### Theme Architecture
- **Design Decision**: Black background with white elements for mathematical clarity
- **Implementation**: Custom CSS overrides and Streamlit theme configuration
- **Rationale**: High contrast improves readability of mathematical expressions and 3D plots

### Mathematical Processing Pipeline
- **Input Validation**: Comprehensive error handling for invalid mathematical expressions
- **Symbol Management**: Consistent use of SymPy symbols across all modules
- **Performance**: Efficient numerical computation using NumPy for large datasets

### Extensibility
The modular architecture allows for easy addition of new features:
- New analysis functions can be added to `AnalysisEngine`
- Additional visualization types can be implemented in `GraphGenerator`
- Extended parsing capabilities can be added to `MathParser`