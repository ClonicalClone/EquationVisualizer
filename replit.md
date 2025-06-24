# 3D Mathematical Grapher

## Overview

This is a pure React-based web application that provides advanced 3D mathematical graphing capabilities. The application uses the entire screen for 3D visualization with floating control cards, allowing users to input mathematical expressions and visualize them as interactive 3D plots with comprehensive analysis features including critical point detection, derivative calculations, and mathematical analysis.

## System Architecture

The application follows a modular React architecture with clear separation of concerns:

- **Frontend**: Pure React with TypeScript and full-screen 3D visualization
- **Mathematical Processing**: Math.js for expression parsing and evaluation
- **Visualization**: Plotly.js for interactive 3D graphics with extreme zoom capabilities
- **UI**: Floating translucent cards with minimizable interface
- **Styling**: Black/white aesthetic with responsive design

## Key Components

### 1. Main Application (`src/App.tsx`)
- **Purpose**: Primary React application orchestration and state management
- **Features**: Full-screen layout, floating card management, real-time equation parsing
- **Architecture Decision**: React with hooks for state management
- **Rationale**: React provides excellent component modularity and real-time updates

### 2. Mathematical Parser (`src/utils/mathParser.ts`)
- **Purpose**: Converts string mathematical expressions into Math.js expressions
- **Features**: Support for various equation formats, implicit multiplication, function recognition
- **Architecture Decision**: Used Math.js as the core mathematical parsing library
- **Rationale**: Math.js provides comprehensive expression parsing and evaluation in JavaScript

### 3. Graph Generator (`src/components/MathGrapher.tsx`)
- **Purpose**: Creates full-screen interactive 3D visualizations using Plotly.js
- **Features**: Black/white color scheme, extreme zoom capabilities, critical point visualization
- **Architecture Decision**: Plotly.js for browser-based 3D rendering
- **Rationale**: Plotly.js offers superior interactive 3D graphics with no server dependency

### 4. Analysis Engine (`src/utils/mathAnalysis.ts`)
- **Purpose**: Performs mathematical analysis (derivatives, critical points, limits)
- **Features**: Derivative calculations, critical point classification, function properties
- **Architecture Decision**: Separate analysis utilities for mathematical operations
- **Rationale**: Modular design allows for easier testing and mathematical feature extension

### 5. Floating Controls (`src/components/FloatingControls.tsx`)
- **Purpose**: Minimizable control interface with transparent design
- **Features**: Equation input, domain controls, visualization options, collapsible interface
- **Architecture Decision**: CSS-based floating cards with backdrop blur
- **Rationale**: Non-intrusive interface that maximizes screen space for visualization

## Data Flow

1. **User Input**: Mathematical expressions entered through Streamlit interface
2. **Parsing**: `MathParser` converts string input to SymPy expressions
3. **Analysis**: `AnalysisEngine` performs mathematical analysis on parsed expressions
4. **Visualization**: `GraphGenerator` creates 3D plots using Plotly
5. **Display**: Streamlit renders the interactive visualizations in the web interface

## External Dependencies

### Core Libraries
- **React 19**: UI framework with hooks
- **TypeScript**: Type-safe JavaScript development
- **Math.js**: Mathematical expression parsing and evaluation
- **Plotly.js**: Interactive 3D visualization library

### Development Tools
- **Node.js 20**: JavaScript runtime environment
- **Vite**: Fast build tool and development server
- **NPM**: Package management

## Deployment Strategy

- **Platform**: Suitable for any Node.js hosting (Vercel, Netlify, local development)
- **Runtime**: Node.js 20 with NPM package management
- **Server**: Vite development server on port 5000
- **Build**: TypeScript compilation with Vite bundling

### Configuration Decisions
- **Port 5000**: Standard development port
- **Host Binding**: 0.0.0.0 for external access
- **Vite Configuration**: Optimized for mathematical libraries (plotly.js-dist, mathjs)

## Changelog

```
Changelog:
- June 24, 2025: Initial Python/Streamlit setup
- June 24, 2025: Converted to pure React application with full-screen 3D graphing
- June 24, 2025: Added floating card interface with Math.js parsing and Plotly.js visualization
- June 24, 2025: Completed React implementation with extreme zoom capabilities and mathematical analysis
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
- **Input Validation**: Real-time error handling for invalid mathematical expressions
- **Symbol Management**: Consistent variable handling across Math.js expressions
- **Performance**: Efficient client-side computation with WebGL-accelerated 3D rendering

### User Interface Design
- **Full-Screen Visualization**: Entire viewport dedicated to 3D graph rendering
- **Floating Cards**: Translucent, minimizable control panels with backdrop blur
- **Extreme Zoom**: Unlimited zoom capabilities for detailed mathematical exploration
- **Responsive Design**: Adaptive layout for different screen sizes

### Extensibility
The modular React architecture allows for easy addition of new features:
- New analysis functions can be added to `mathAnalysis.ts`
- Additional visualization types can be implemented in `MathGrapher.tsx`
- Extended parsing capabilities can be added to `mathParser.ts`
- New floating panels can be created as separate components

## Local Development Setup

To run this project locally:

1. **Prerequisites**: Node.js 20+ and NPM
2. **Install dependencies**: `npm install`
3. **Development server**: `npm run dev`
4. **Build for production**: `npm run build`

The application will run on `http://localhost:5000` with full functionality including extreme zoom, floating controls, and mathematical analysis.