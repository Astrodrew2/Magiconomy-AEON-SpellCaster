# Magiconomy AEON SpellCaster

## Overview
The Magiconomy AEON SpellCaster is a Streamlit-based web application for generating and visualizing spells within the AEON universe. It creates interactive 3D orbital diagrams using matplotlib to represent spell compositions with glyphs, modifiers, and various magical properties.

## Project Status
Successfully configured for Replit environment on November 29, 2025.

## Recent Changes
- **2025-11-29**: Initial setup for Replit environment
  - Installed Python 3.11 and dependencies (streamlit, matplotlib, numpy, tabulate)
  - Configured Streamlit to bind to 0.0.0.0:5000 with CORS disabled for Replit proxy
  - Fixed bug: initialized `rtcEnergy` variable in atomwords.py to prevent unbound access
  - Set up workflow for Streamlit app on port 5000 with webview output
  - Configured autoscale deployment for production
  - Created .gitignore for Python artifacts

## Project Architecture

### Main Files
- **MagiconomyApp.py**: Main Streamlit application interface with sidebar controls
- **atomwords.py**: Core visualization engine that generates 3D orbital spell diagrams
- **glyphdict.py**: Dictionary of spell glyphs with properties (level, section, AP, range, etc.)
- **modsdict.py**: Dictionary of spell modifiers that enhance glyphs

### Configuration
- **.streamlit/config.toml**: Streamlit server configuration for Replit environment
- **pyproject.toml**: Python project dependencies managed by uv

### Key Features
- Interactive glyph selection from multiple domains (LEY, END, DEATH, DARK SHAMAN, SHAMAN, DRUID)
- Modifier application with visual indicators
- Range and range type calculations
- Quicken and channeling mechanics
- AP (Action Points) and Energy cost calculations
- 3D visualization with sectors and orbital levels

## Technical Details

### Dependencies
- streamlit: Web application framework
- matplotlib: 3D visualization and plotting
- numpy: Numerical computations
- tabulate: Formatted table output

### Ports
- Development: Port 5000 (bound to 0.0.0.0)
- Production: Port 5000 (autoscale deployment)

### Deployment
- Target: Autoscale (stateless web application)
- Command: `streamlit run MagiconomyApp.py --server.port=5000 --server.address=0.0.0.0`

## Development Notes
- The application uses Streamlit's session state for interactivity
- 3D plots are generated using matplotlib's 3D projection
- The app supports various spell mechanics including range increases, quickening, and modifiers
- All calculations are performed in real-time based on user input
