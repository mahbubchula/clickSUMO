# 🚗 ClickSUMO

**One-Click Traffic Simulation Made Easy**

Created by **Mahbub Hassan**
Graduate Student & Non Asean Scholar
Department of Civil Engineering, Faculty of Engineering
Chulalongkorn University, Bangkok, Thailand

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](docs/CONTRIBUTING.md)

</div>

> **Democratizing Traffic Simulation for Everyone**

**ClickSUMO** is an open-source, AI-powered web platform that makes SUMO (Simulation of Urban Mobility) traffic simulation accessible to researchers, students, and practitioners with just one click—no programming required.

Whether you're designing traffic networks, analyzing vehicle flows, or teaching transportation concepts, ClickSUMO provides an intuitive one-click interface to create, configure, and simulate complex traffic scenarios instantly.

---

## ⚡ Try It Online

**🌐 [Launch ClickSUMO on Streamlit Cloud](https://clicksumo.streamlit.app/)** - **Live Now!** 🚀

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://clicksumo.streamlit.app/)

> **Why "ClickSUMO"?** Because traffic simulation should be as simple as one click!

Or install locally:

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- SUMO simulation software (optional, for running simulations)
- Git (for cloning the repository)

### Installation & Setup

**Option 1: Automated Setup (Recommended)**
```bash
# Clone the repository
git clone https://github.com/mahbubchula/clickSUMO.git
cd sumo-forge

# Run automated setup script
python setup.py
```

**Option 2: Manual Setup**

1. **Clone or navigate to the project**
   ```bash
   git clone https://github.com/mahbubchula/clickSUMO.git
   cd sumo-forge
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Launch the application**
   ```bash
   streamlit run app.py
   ```

   The application will open in your default browser at `http://localhost:8501`

---

## 🚢 Deployment

Want to deploy ClickSUMO online? See our comprehensive [DEPLOYMENT.md](docs/DEPLOYMENT.md) guide for:
- 🟣 Streamlit Community Cloud (free, easiest)
- 🐳 Docker deployment
- ☁️ Heroku, Railway, Google Cloud Run
- 🔧 Production configuration tips

---

## 📁 Project Structure

```
sumo-forge/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── setup.py                  # Automated setup script
├── README.md                 # This file
├── LICENSE                   # MIT License
│
├── src/                      # Source code package
│   ├── __init__.py
│   ├── core/                 # Core XML generation engines
│   │   ├── __init__.py
│   │   └── xml_generators.py # Network, route & config generators
│   ├── network/              # Network creation & templates
│   │   ├── __init__.py
│   │   └── templates.py      # Pre-built network templates
│   ├── demand/               # Traffic demand generation
│   │   └── __init__.py
│   ├── signals/              # Traffic signal configuration
│   │   └── __init__.py
│   ├── analysis/             # Simulation output analysis
│   │   └── __init__.py
│   └── utils/                # Utility functions
│       └── __init__.py
│
├── outputs/                  # Generated simulation files
│   ├── .gitkeep              # Keeps folder in git
│   ├── network.nod.xml       # Node definitions
│   ├── network.edg.xml       # Edge (road) definitions
│   ├── network.rou.xml       # Route definitions
│   └── network.tll.xml       # Traffic light logic
│
├── docs/                     # Documentation
│   ├── CHANGELOG.md          # Version history
│   ├── CONTRIBUTING.md       # Contribution guidelines
│   ├── CODE_OF_CONDUCT.md    # Community standards
│   ├── DEPLOYMENT.md         # Deployment guide
│   └── SECURITY_GUIDE.md     # Security best practices
│
├── .streamlit/               # Streamlit configuration
│   ├── config.toml           # UI theme & settings
│   └── secrets.toml.example  # Secrets template
│
└── .env.example              # Environment variables template
```

---

## 🎯 Features & Roadmap

### ✅ Phase 1 (Completed)
**Core Network Creation & Simulation File Generation**
- [x] **Network Studio** with 6 pre-built templates:
  - 4-way intersection (cross junction)
  - 3-way T-intersection
  - Roundabout
  - Grid network layout
  - Arterial corridor
  - Highway segment
- [x] Visual XML file generation (nodes, edges, traffic lights)
- [x] Basic traffic demand generator
- [x] Modern Streamlit web interface with real-time preview
- [x] One-click file generation & export

### ✅ Phase 2 (Completed - NEW!)
**Advanced Analysis & Optimization Tools**
- [x] **Traffic Signal Designer** with:
  - 🎨 Visual phase editor for custom signal timing
  - ⏱️ Webster's optimization method for minimal delay
  - 🔄 Signal coordination & green wave calculation
  - 📊 Intersection capacity analysis
- [x] **Output Analyzer** with:
  - 📤 XML file upload & parsing (tripinfo, emissions)
  - 📊 Automatic KPI calculation (travel time, delay, emissions)
  - 📈 Interactive Plotly charts & visualizations
  - 📋 Export to CSV, Excel, and LaTeX tables
- [x] **AI Assistant** powered by Groq:
  - 💬 Natural language chat interface
  - 🎯 AI-powered scenario generator
  - 🔧 Intelligent troubleshooter
  - 📝 Parameter recommendations

### 📋 Phase 3 (Planned)
- [ ] Reinforcement Learning (RL) environment generator
- [ ] Real-time simulation monitoring dashboard
- [ ] OpenStreetMap (OSM) network import
- [ ] Publication-ready chart exports with templates
- [ ] Batch simulation runner with parameter sweeps

---

## 📖 Usage Guide

### Workflow Overview
ClickSUMO simplifies the traffic simulation process into five main steps:

```
1. Create Network  →  2. Add Traffic  →  3. Optimize Signals  →  4. Run Simulation  →  5. Analyze Results
```

### Step 1: Create a Network

1. Launch the application and navigate to **Network Studio**
2. Select a network template from the available options:
   - Each template comes with sensible defaults
   - Suitable for research, education, and real-world scenarios
3. Configure your network parameters:
   - **Arm Length**: Length of each road segment (meters)
   - **Number of Lanes**: Traffic capacity per direction
   - **Speed Limit**: Maximum allowed speed (km/h)
   - **Signal Timing**: Traffic light phases and durations
4. Click **Generate Network** to create the simulation files
5. Generated files are automatically saved to the `outputs/` folder

### Step 2: Add Traffic Demand

1. Navigate to **Demand Generator**
2. Define your vehicle fleet:
   - Use pre-configured vehicle types or create custom ones
   - Specify vehicle parameters (length, max speed, acceleration)
3. Create traffic flows:
   - Select source edge (origin)
   - Select destination edge (destination)
   - Set traffic volume (vehicles per hour)
   - Specify time period (start and end times)
4. Click **Generate Route File** to create traffic patterns
5. Routes are saved to `outputs/network.rou.xml`

### Step 3: Optimize Traffic Signals (NEW!)

1. Navigate to **Signal Designer**
2. Choose your optimization approach:
   - **Phase Editor**: Manually design signal phases
   - **Webster's Optimization**: Auto-calculate optimal timing for minimal delay
   - **Coordination**: Create green waves for arterial corridors
   - **Capacity Analysis**: Check if your intersection can handle the traffic
3. Generate optimized signal timing files

### Step 4: Run in SUMO

Once your files are generated, run the simulation using SUMO:

1. **Convert network files to SUMO format:**
   ```bash
   netconvert --node-files=outputs/network.nod.xml \
              --edge-files=outputs/network.edg.xml \
              --output-file=outputs/network.net.xml
   ```

2. **Launch the simulation:**
   ```bash
   sumo-gui -c outputs/network.sumocfg
   ```

3. **For batch simulations (no GUI):**
   ```bash
   sumo -c outputs/network.sumocfg --tripinfo-output outputs/tripinfo.xml
   ```

### Step 5: Analyze Results (NEW!)

1. Navigate to **Output Analyzer**
2. Upload your simulation output files:
   - `tripinfo.xml` - Vehicle trip information
   - `emissions.xml` - Emissions data (optional)
3. View interactive visualizations:
   - Travel time distributions
   - Waiting time analysis
   - Emissions breakdown
   - Traffic timeline
4. Export analysis:
   - Download as CSV or Excel
   - Generate LaTeX tables for publications
   - View statistical summaries

### Bonus: Get AI Help!

1. Navigate to **AI Assistant**
2. Chat with AI about your simulation challenges
3. Generate scenarios from natural language descriptions
4. Get troubleshooting help for issues

---

## 🔧 Development & Contributing

### Environment Setup for Developers

```bash
# Clone the repository
git clone https://github.com/mahbubchula/clickSUMO.git
cd sumo-forge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Optional dev tools
```

### Project Structure for Developers

- **`src/core/`**: Core XML generation logic - handles all SUMO file creation
- **`src/network/`**: Network templates and management
- **`src/demand/`**: Traffic demand and routing algorithms
- **`src/signals/`**: Traffic signal timing and optimization
- **`src/analysis/`**: Output analysis and visualization
- **`app.py`**: Main Streamlit application - entry point

### Running Tests
```bash
pytest tests/ -v
```

### Code Style
```bash
black src/
flake8 src/
```

---

## 📚 Learning Resources

### Official Documentation
- 📖 [SUMO Official Documentation](https://sumo.dlr.de/docs/) - Complete SUMO reference
- 🎓 [Streamlit Documentation](https://docs.streamlit.io/) - Framework for our UI
- 🤖 [TraCI Python API](https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html) - Control simulations with Python

### Tutorials & Examples
- [SUMO Tutorial](https://sumo.dlr.de/docs/tutorial/) - Official SUMO tutorials
- [TraCI Examples](https://github.com/eclipse/sumo/tree/master/tools/traci/examples) - Python simulation examples

### Traffic Engineering Concepts
- [SUMO XML Format Guide](https://sumo.dlr.de/docs/Networks/Building_Networks/) - Understand network files
- [Signal Timing Basics](https://sumo.dlr.de/docs/Simulation/Traffic_Lights/) - Traffic signal configuration

---

## 🤝 Contributing

We welcome contributions from the community! Whether it's:
- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🔧 Code contributions

Please read our [CONTRIBUTING.md](docs/CONTRIBUTING.md) guide to get started.

### Quick Contribution Guide
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author & Contact

**Mahbub Hassan**
- 🎓 Graduate Student & Non Asean Scholar
- 🏫 Department of Civil Engineering
- 🏛️ Faculty of Engineering, [Chulalongkorn University](https://www.chula.ac.th/)
- 📍 Bangkok, Thailand
- 📧 Email: [6870376421@student.chula.ac.th](mailto:6870376421@student.chula.ac.th)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**What this means:**
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ℹ️ License and copyright notice required

---

## 🙏 Acknowledgments

- 🚗 **SUMO Team** - For the excellent traffic simulation platform
- 🎨 **Streamlit Team** - For making data apps accessible
- 🎓 **Chulalongkorn University** - Supporting this research
- 👥 **Contributors** - For improving this project

---

## 💬 Support & Feedback

Have questions or feedback? We'd love to hear from you!

- � **Report Issues**: [GitHub Issues](https://github.com/mahbubchula/clickSUMO/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mahbubchula/clickSUMO/discussions)
- 📧 **Email**: [6870376421@student.chula.ac.th](mailto:6870376421@student.chula.ac.th)
- ⭐ **Star this repo** if you find it useful!

---

## 📊 Project Status

- ✅ **Phase 1**: Core functionality complete
- 🚧 **Phase 2**: In active development
- 📋 **Phase 3**: Planned for future release

---

## 🌟 Star History

If you find this project helpful, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=mahbubchula/clickSUMO&type=Date)](https://star-history.com/#mahbubchula/clickSUMO&Date)

---

<div align="center">

**Made with ❤️ for the transportation research & education community**

*Last updated: January 2026*

[⬆ Back to Top](#-simplesumo)

</div>

.  
 