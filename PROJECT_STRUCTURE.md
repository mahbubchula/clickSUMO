# 📁 ClickSUMO Project Structure Guide

This document explains the organization and purpose of every file and folder in the ClickSUMO project.

## 🏗️ Directory Overview

```
clicksumo/
├── 📄 Core Application Files
├── 📦 Source Code (src/)
├── 📝 Documentation (docs/)
├── 🗂️ Configuration Files
├── 📤 Output Directory (outputs/)
└── 🔧 Environment (venv/)
```

---

## 📄 Root Level Files

### Essential Application Files

| File | Purpose |
|------|---------|
| **app.py** | Main Streamlit application - **START HERE** to run the app |
| **requirements.txt** | Python package dependencies |
| **setup.py** | Automated setup script for first-time installation |
| **README.md** | Main documentation with quick start guide |
| **LICENSE** | MIT License for the project |

### Configuration Files

| File | Purpose |
|------|---------|
| **.env.example** | Template for environment variables (copy to `.env`) |
| **.gitignore** | Git exclusions (prevents sensitive files from being committed) |
| **packages.txt** | System-level dependencies for Streamlit Cloud deployment |

---

## 📦 Source Code Directory (`src/`)

All Python source code is organized in modules:

```
src/
├── __init__.py              # Package initialization
│
├── core/                    # ⚙️ Core Engine
│   ├── __init__.py
│   └── xml_generators.py    # XML generators for SUMO files (761 lines)
│                            # Classes: Node, Edge, Phase, TrafficLight,
│                            # VehicleType, Flow, NetworkGenerator,
│                            # RouteGenerator, ConfigGenerator
│
├── network/                 # 🛣️ Network Management
│   ├── __init__.py
│   └── templates.py         # Pre-built network templates (727 lines)
│                            # 6 templates: intersection, T-junction,
│                            # roundabout, grid, arterial, highway
│
├── demand/                  # 🚗 Traffic Demand
│   └── __init__.py          # Placeholder for future demand generation
│
├── signals/                 # 🚦 Traffic Signals
│   └── __init__.py          # Placeholder for signal optimization
│
├── analysis/                # 📊 Output Analysis
│   └── __init__.py          # Placeholder for analysis tools
│
└── utils/                   # 🔧 Utilities
    └── __init__.py          # Placeholder for utility functions
```

### What Each Module Does

**core/** - The Heart of ClickSUMO
- Contains all XML generation logic
- Converts Python objects to SUMO XML files
- Handles network (.nod.xml, .edg.xml), routes (.rou.xml), and config (.sumocfg)

**network/** - Network Templates
- Pre-configured network layouts
- Functions: `list_templates()`, `create_network(template_name, params)`
- Used by the "Network Studio" page in the UI

**demand/**, **signals/**, **analysis/**, **utils/**
- Currently placeholders for future Phase 3 features
- Each has `__init__.py` to mark as Python package

---

## 📝 Documentation Directory (`docs/`)

All project documentation beyond the main README:

```
docs/
├── README.md              # Documentation index
├── CHANGELOG.md           # Version history and release notes
├── CONTRIBUTING.md        # How to contribute to the project
├── CODE_OF_CONDUCT.md     # Community guidelines
├── DEPLOYMENT.md          # Deployment instructions (Streamlit Cloud, Docker, etc.)
└── SECURITY_GUIDE.md      # Security best practices
```

**Why a separate docs/ folder?**
- Keeps root directory clean
- Groups all documentation together
- Follows GitHub/GitLab best practices
- Makes navigation easier for contributors

---

## 📤 Output Directory (`outputs/`)

Where generated SUMO files are saved:

```
outputs/
├── .gitkeep               # Keeps empty folder in git
├── network.nod.xml        # Node definitions (junctions)
├── network.edg.xml        # Edge definitions (roads)
├── network.rou.xml        # Route definitions (traffic flows)
└── network.tll.xml        # Traffic light logic (optional)
```

**Note:** The `.gitkeep` file ensures the `outputs/` folder is tracked by git even when empty. All `.xml` files are gitignored to avoid committing large simulation outputs.

---

## 🔧 Configuration Directory (`.streamlit/`)

Streamlit-specific configuration:

```
.streamlit/
├── config.toml            # UI theme, server settings, browser config
└── secrets.toml.example   # Template for API keys and secrets
```

**config.toml** sets:
- Theme colors (dark mode)
- Server port and headless mode
- File upload limits
- Browser auto-open

**secrets.toml.example** shows how to configure:
- Groq API key for AI Assistant
- Other secrets (copy to `secrets.toml` for local use)

---

## 🔐 Environment Files

| File | Purpose | Tracked in Git? |
|------|---------|-----------------|
| `.env.example` | Template showing required variables | ✅ Yes |
| `.env` | Your actual API keys and secrets | ❌ No (gitignored) |

**Setup:**
1. Copy `.env.example` to `.env`
2. Fill in your actual API keys
3. Never commit `.env` to git (it's in `.gitignore`)

---

## 🎨 File Organization Principles

### Why This Structure?

1. **Separation of Concerns**
   - Code (`src/`) separate from docs (`docs/`)
   - Configuration files in dedicated folders
   - Generated files isolated in `outputs/`

2. **Scalability**
   - Modular structure allows adding new features easily
   - Each module has clear responsibility
   - Easy to find and modify specific functionality

3. **Best Practices**
   - Follows Python package conventions
   - Matches Streamlit deployment requirements
   - Compatible with GitHub/GitLab standards

4. **Clarity**
   - Clear naming (no abbreviations)
   - Logical grouping
   - Self-documenting structure

---

## 🚀 Quick Reference

### I Want To...

**Run the application:**
```bash
streamlit run app.py
```

**Understand how it works:**
1. Start with `README.md`
2. Read `src/core/xml_generators.py` (core logic)
3. Check `src/network/templates.py` (examples)

**Add a new network template:**
1. Edit `src/network/templates.py`
2. Add your template function
3. Update the template list

**Deploy the app:**
1. Read `docs/DEPLOYMENT.md`
2. Choose your platform
3. Follow step-by-step instructions

**Contribute:**
1. Read `docs/CONTRIBUTING.md`
2. Fork the repository
3. Make your changes
4. Submit a pull request

---

## 📊 File Count Summary

| Category | Count | Files |
|----------|-------|-------|
| Root Config/Docs | 5 | app.py, README.md, requirements.txt, setup.py, packages.txt |
| Source Code | 9 | All .py files in src/ |
| Documentation | 6 | All .md files in docs/ |
| Configuration | 4 | .env.example, .gitignore, .streamlit/* |
| **Total** | **24** | Excluding outputs and venv |

**Before cleanup:** 30+ files (including 8 backup app.py files, 6 redundant docs)
**After cleanup:** 24 essential files only

---

## 🎯 What We Removed

**Deleted Files:**
- ❌ `test_design.py` - CSS test file, not needed
- ❌ `nul` - Empty file (likely accident)
- ❌ `CHECKLIST.md` - Internal deployment checklist
- ❌ `DEPLOYMENT_SUMMARY.md` - Redundant with DEPLOYMENT.md
- ❌ `QUICK_REFERENCE.md` - Info integrated into README
- ❌ `RELEASE_NOTES_v0.2.0.md` - Moved to CHANGELOG.md
- ❌ 8 backup files - `app_backup.py`, `app_clean.py`, etc.

**Removed Folders:**
- ❌ `templates/` - Was empty

**Result:** Cleaner, more professional project structure ✨

---

## 💡 Tips for Developers

### Adding New Features

1. **New module:** Add to `src/` with descriptive name
2. **New template:** Add function to `src/network/templates.py`
3. **New page:** Add section in `app.py` (or create `pages/` folder for multi-page)
4. **New docs:** Add to `docs/` folder

### File Naming Conventions

- **Python files:** `snake_case.py` (e.g., `xml_generators.py`)
- **Documentation:** `UPPERCASE.md` (e.g., `README.md`)
- **Config files:** lowercase (e.g., `config.toml`)
- **Folders:** `lowercase` (e.g., `src/`, `docs/`)

---

**Questions?** Check [README.md](README.md) or open an [issue](https://github.com/yourusername/clicksumo/issues).
