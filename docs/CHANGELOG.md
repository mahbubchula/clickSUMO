# Changelog

All notable changes to ClickSUMO will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Reinforcement Learning environment generator
- OpenStreetMap network import
- Real-time simulation monitoring
- Batch simulation runner with parameter sweeps

## [0.2.0] - 2025-12-31

### Added - Phase 2 Features!
- 🚦 **Signal Designer** - Complete traffic signal optimization suite:
  - Visual phase editor with customizable signal states
  - Webster's optimization method for minimal delay calculation
  - Signal coordination for green wave progression
  - Intersection capacity analysis with LOS estimates
- 📊 **Output Analyzer** - Advanced simulation analysis:
  - XML file upload and parsing (tripinfo.xml, emissions.xml)
  - Automatic KPI calculations (travel time, delay, emissions)
  - Interactive Plotly visualizations (histograms, box plots, timelines)
  - Performance analysis by vehicle type
  - Emissions breakdown and environmental impact
  - Export to CSV, Excel (.xlsx), and LaTeX formats
- 🤖 **AI Assistant** - Groq-powered intelligent helper:
  - Natural language chat interface for SUMO questions
  - AI-powered scenario generator from text descriptions
  - Intelligent troubleshooter with diagnosis and solutions
  - Context-aware recommendations for parameters
  - Quick tips database for common issues

### Enhanced
- Added openpyxl dependency for Excel export functionality
- Improved error handling across all new features
- Updated requirements.txt with new dependencies
- Enhanced documentation with Phase 2 features

### Fixed
- Import statements properly scoped in Signal Designer
- XML parsing error handling in Output Analyzer

## [0.1.0] - 2025-12-31

### Added
- ✨ Initial release of ClickSUMO
- 🛣️ Network Studio with 6 pre-built templates:
  - 4-way intersection
  - 3-way T-intersection
  - Roundabout
  - Grid network
  - Arterial corridor
  - Highway segment
- 🚗 Basic traffic demand generator
  - Custom vehicle types
  - Traffic flow configuration
  - Route file generation
- 📁 XML file generation for SUMO
  - Node files (.nod.xml)
  - Edge files (.edg.xml)
  - Route files (.rou.xml)
  - Traffic light files (.tll.xml)
- 🎨 Modern Streamlit web interface
- 📥 File download functionality (individual and ZIP)
- 📊 Session state management
- 🎨 Custom CSS styling
- 📝 Comprehensive documentation
  - README with installation and usage guide
  - DEPLOYMENT guide for various platforms
  - CONTRIBUTING guidelines
  - LICENSE (MIT)

### Infrastructure
- Python package structure with modular design
- Core XML generators module
- Network templates system
- Streamlit configuration
- Environment variable management
- .gitignore for Python/Streamlit projects

---

## Release Notes

### Version 0.2.0 - "Professional Release" 🚀

**Major Update!** ClickSUMO is now a complete, production-ready traffic simulation toolkit!

This release adds three major professional features that transform ClickSUMO from a basic network generator into a comprehensive traffic engineering suite:

**🚦 Signal Designer**
Design and optimize traffic signals like a pro! Use Webster's method to calculate optimal cycle lengths that minimize delay, coordinate signals for green waves, and analyze intersection capacity. Perfect for research and real-world applications.

**📊 Output Analyzer**
Upload your simulation results and instantly get professional analysis with interactive charts, KPI calculations, and publication-ready exports. Supports CSV, Excel, and LaTeX outputs.

**🤖 AI Assistant**
Get intelligent help powered by Groq's LLMs. Chat naturally about traffic simulation, generate scenarios from descriptions, and troubleshoot issues with AI-powered diagnosis.

**Target Users:**
- Transportation researchers writing papers
- Traffic engineers optimizing real intersections
- Graduate students learning simulation
- Anyone needing professional SUMO analysis tools

### Version 0.1.0 - "Foundation Release"

This is the first public release of ClickSUMO, providing the core functionality for creating SUMO traffic simulation files without programming knowledge.

---

[Unreleased]: https://github.com/yourusername/clicksumo/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/yourusername/clicksumo/releases/tag/v0.2.0
[0.1.0]: https://github.com/yourusername/clicksumo/releases/tag/v0.1.0
