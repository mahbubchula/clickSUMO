"""
ClickSUMO: One-Click Traffic Simulation
========================================

Main Streamlit application for ClickSUMO.

Author: Mahbub Hassan
Graduate Student & Non Asean Scholar
Department of Civil Engineering
Faculty of Engineering
Chulalongkorn University
Bangkok, Thailand

Copyright © 2026 Mahbub Hassan
"""

import streamlit as st
import os
import sys
import zipfile
import io
import html
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core import (
    Node, Edge, Phase, TrafficLight, VehicleType, Flow,
    NetworkGenerator, RouteGenerator, ConfigGenerator,
    kmh_to_ms
)
from src.network import list_templates, create_network

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="ClickSUMO",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# PREMIUM DESIGN SYSTEM - ClickSUMO v1.0 (Nebula AI Theme)
# Theme: Deep Space & Gradient Violet
# Style: Glassmorphism & Glow
# =============================================================================

st.markdown("""
<style>
/* =========================================================================
   SIMPLESUMO AI THEME v8.0 - "NEBULA"
   ========================================================================= */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* RESET & BASE */
*, *::before, *::after {
    box-sizing: border-box;
}

html, body, .stApp {
    background-color: #050505; /* Deep Void */
    color: #f8fafc;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* MAIN CONTAINER */
.main .block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: 1200px;
    background-color: transparent;
}

/* Hide default Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* TYPOGRAPHY */
h1 {
    font-size: 2.75rem;
    font-weight: 700;
    background: linear-gradient(to right, #ffffff 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-top: 2.5rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 0.5rem;
}

h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: #cbd5e1;
}

p, li, span {
    color: #94a3b8; /* Soft Slate */
    line-height: 1.7;
}

strong, b {
    color: #ffffff;
    font-weight: 600;
}

/* SIDEBAR STYLING */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1014 0%, #050505 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.15);
    padding: 1.5rem;
}

[data-testid="stSidebar"] > div:first-child {
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.5rem;
}

/* SIDEBAR NAVIGATION (RADIO BUTTONS) */
[data-testid="stSidebar"] .stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

[data-testid="stSidebar"] .stRadio > div > label {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 0.95rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    color: #94a3b8;
}

[data-testid="stSidebar"] .stRadio > div > label:hover {
    background-color: rgba(255, 255, 255, 0.08);
    color: #ffffff;
    transform: translateX(6px);
    border-color: rgba(255,255,255,0.1);
}

/* ACTIVE STATE - NEBULA GLOW */
[data-testid="stSidebar"] .stRadio > div > label[data-selected="true"] {
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    color: #ffffff;
    font-weight: 600;
    border: 1px solid rgba(139, 92, 246, 0.5);
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    transform: translateX(6px);
}

/* INPUT FIELDS - Cyberpunk Feel */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #0f1014;
    border: 1px solid #2d3748;
    color: #f8fafc;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.95rem;
    transition: all 0.2s ease;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #8b5cf6; /* Violet Focus */
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15);
    outline: none;
    background-color: #13141a;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #4a5568;
}

/* LABELS */
label {
    color: #e2e8f0;
    font-weight: 500;
    font-size: 0.9rem;
}

/* SELECT BOX & DROPDOWN */
div[data-baseweb="select"] {
    background-color: #0f1014;
    border: 1px solid #2d3748;
    border-radius: 10px;
}

div[data-baseweb="select"] > div {
    background-color: #0f1014;
    color: #f8fafc;
}

[data-baseweb="popover"] {
    background-color: #13141a !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 12px !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
}

div[role="option"] {
    background-color: transparent !important;
    color: #cbd5e1 !important;
}

div[role="option"]:hover, div[role="option"][aria-selected="true"] {
    background-color: rgba(99, 102, 241, 0.1) !important;
    color: #ffffff !important;
}

/* BUTTONS - Nebula Gradient */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: #ffffff;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
}

/* PRIMARY BUTTON OVERRIDE */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
}

/* DOWNLOAD BUTTON */
.stDownloadButton > button {
    background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.25);
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);
    box-shadow: 0 8px 20px rgba(6, 182, 212, 0.4);
}

/* TABS - Glassy */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 6px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #64748b;
    font-weight: 500;
    padding: 10px 20px;
    transition: all 0.2s;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: #f8fafc;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.2);
}

/* EXPANDERS - Glassy */
.stExpander {
    background-color: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    color: #f8fafc;
}

.stExpander header {
    color: #e2e8f0;
    font-weight: 600;
}

/* METRICS - Glassy */
[data-testid="stMetricContainer"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.25rem;
    backdrop-filter: blur(10px);
}

[data-testid="stMetricValue"] {
    background: linear-gradient(to right, #8b5cf6, #d946ef);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    font-weight: 600;
}

/* DATAFRAME */
.stDataFrame {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    overflow: hidden;
    background: #0f1014;
}

.stDataFrame th {
    background-color: #13141a;
    color: #e2e8f0;
    font-weight: 600;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.stDataFrame td {
    color: #cbd5e1;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.stDataFrame tr:hover td {
    background-color: rgba(99, 102, 241, 0.05);
}

/* ALERTS */
.stAlert {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    backdrop-filter: blur(5px);
    color: #f8fafc;
}

/* FILE UPLOADER */
.stFileUploader {
    border: 2px dashed rgba(139, 92, 246, 0.3);
    border-radius: 12px;
    background-color: rgba(99, 102, 241, 0.03);
    transition: all 0.2s;
}

.stFileUploader:hover {
    border-color: #8b5cf6;
    background-color: rgba(99, 102, 241, 0.08);
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
::-webkit-scrollbar-track {
    background: #050505;
}
::-webkit-scrollbar-thumb {
    background: #2d3748;
    border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
    background: #4a5568;
}

/* CUSTOM UTILITY CLASSES */

/* Feature Cards - Glassmorphism */
.feature-card {
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 2rem;
    transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    border-color: rgba(139, 92, 246, 0.3);
}

/* Info Boxes - AI Tinted */
.info-box {
    background-color: rgba(99, 102, 241, 0.1);
    border-left: 4px solid #6366f1;
    padding: 1.25rem;
    border-radius: 4px;
    color: #e2e8f0;
}

.success-box {
    background-color: rgba(16, 185, 129, 0.1);
    border-left: 4px solid #10b981;
    padding: 1.25rem;
    border-radius: 4px;
    color: #e2e8f0;
}

.warning-box {
    background-color: rgba(245, 158, 11, 0.1);
    border-left: 4px solid #f59e0b;
    padding: 1.25rem;
    border-radius: 4px;
    color: #e2e8f0;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
    margin: 2.5rem 0;
    border: none;
}

/* Code Block */
code {
    background-color: #0f1014;
    color: #e2e8f0;
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9em;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Link Buttons */
.stLinkButton a {
    background-color: rgba(255,255,255,0.05);
    color: #f8fafc;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    transition: all 0.2s;
}
.stLinkButton a:hover {
    background-color: rgba(99, 102, 241, 0.2);
    border-color: #6366f1;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
}

</style>
""", unsafe_allow_html=True)


# =============================================================================
# Session State Initialization
# =============================================================================

if 'network' not in st.session_state:
    st.session_state.network = None
if 'routes' not in st.session_state:
    st.session_state.routes = None
if 'generated_files' not in st.session_state:
    st.session_state.generated_files = []
if 'vehicle_types' not in st.session_state:
    st.session_state.vehicle_types = []
if 'flows' not in st.session_state:
    st.session_state.flows = []


# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================

with st.sidebar:
    st.markdown("## 🚗 ClickSUMO")
    st.markdown('<p style="color: #8b5cf6; font-size: 0.85rem; font-weight: 700; margin-top: -10px; letter-spacing: 0.1em;">AI-POWERED</p>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠 Home", "🛣️ Network Studio", "🚗 Demand Generator",
         "🚦 Signal Designer", "📊 Output Analyzer", "📚 Documentation", "🤖 AI Assistant"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Quick Stats")

    if st.session_state.network:
        st.success("✅ Network Ready")
    else:
        st.info("⏳ No network yet")

    if st.session_state.routes:
        st.success("✅ Routes Ready")
    else:
        st.info("⏳ No routes yet")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📁 Generated Files")

    if st.session_state.generated_files:
        for f in st.session_state.generated_files:
            st.markdown(f"📄 **{f}**")
    else:
        st.info("No files generated yet")

    # Project Management
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 💾 Project Manager")

    from src.project_manager import ProjectManager
    pm = ProjectManager()

    # Quick save/load buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save", use_container_width=True):
            st.session_state.show_save_dialog = True

    with col2:
        if st.button("📂 Load", use_container_width=True):
            st.session_state.show_load_dialog = True

    # Save dialog
    if st.session_state.get('show_save_dialog', False):
        with st.form("save_project_form"):
            project_name = st.text_input("Project Name", value=f"project_{datetime.now().strftime('%Y%m%d_%H%M')}")
            description = st.text_area("Description (optional)", height=100)

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Save", use_container_width=True):
                    if pm.save_project(project_name, description):
                        st.success(f"✅ Project '{project_name}' saved!")
                        st.session_state.show_save_dialog = False
                        st.rerun()
                    else:
                        st.error("Failed to save project")
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_save_dialog = False
                    st.rerun()

    # Load dialog
    if st.session_state.get('show_load_dialog', False):
        projects = pm.list_projects()

        if projects:
            st.markdown("**Saved Projects:**")
            selected_project = st.selectbox(
                "Select project:",
                options=[p['name'] for p in projects],
                format_func=lambda x: f"{x} ({[p for p in projects if p['name']==x][0]['created'][:10]})"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📂 Load Selected", use_container_width=True):
                    if pm.load_project(selected_project):
                        st.success(f"✅ Project '{selected_project}' loaded!")
                        st.session_state.show_load_dialog = False
                        st.rerun()
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_load_dialog = False
                    st.rerun()
        else:
            st.info("No saved projects yet")
            if st.button("Close"):
                st.session_state.show_load_dialog = False
                st.rerun()

    # Footer
    st.markdown('<div class="divider" style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center;'>
        <p style='color: #94a3b8; font-size: 0.8rem; letter-spacing: 0.05em; font-weight: 600;'>NEBULA v8.0</p>
        <p style='color: #64748b; font-size: 0.75rem;'>© 2025 Mahbub Hassan</p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# HOME PAGE
# =============================================================================

def show_home():
    st.markdown('<h1>🚗 ClickSUMO</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.2rem; color: #cbd5e1; font-weight: 500;">Next-Gen Traffic Simulation</p>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #8b5cf6;">🛣️ Network Studio</h3>
            <p style="color: #e2e8f0; font-size: 1rem;">Create road networks visually:</p>
            <ul style="color: #94a3b8; margin-top: 1rem;">
                <li style="margin-bottom: 0.5rem;">Pre-built templates</li>
                <li style="margin-bottom: 0.5rem;">Custom intersections</li>
                <li style="margin-bottom: 0.5rem;">OpenStreetMap import</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #6366f1;">🚗 Demand Generator</h3>
            <p style="color: #e2e8f0; font-size: 1rem;">Define traffic patterns:</p>
            <ul style="color: #94a3b8; margin-top: 1rem;">
                <li style="margin-bottom: 0.5rem;">Vehicle types</li>
                <li style="margin-bottom: 0.5rem;">Traffic flows</li>
                <li style="margin-bottom: 0.5rem;">OD matrices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #06b6d4;">📊 Output Analyzer</h3>
            <p style="color: #e2e8f0; font-size: 1rem;">Analyze results:</p>
            <ul style="color: #94a3b8; margin-top: 1rem;">
                <li style="margin-bottom: 0.5rem;">Travel time & delay</li>
                <li style="margin-bottom: 0.5rem;">Emissions</li>
                <li style="margin-bottom: 0.5rem;">Publication charts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Quick Start Guide
    st.markdown("## 🚀 Quick Start Guide")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #a78bfa;">📋 Step 1: Create Network</h4>
            <p style="color: #e2e8f0;">Go to Network Studio → Choose template → Configure → Generate</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <h4 style="color: #a78bfa;">📋 Step 2: Add Demand</h4>
            <p style="color: #e2e8f0;">Go to Demand Generator → Define vehicles → Add flows → Generate</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #a78bfa;">📋 Step 3: Download Files</h4>
            <p style="color: #e2e8f0;">Download all generated XML files to your computer</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <h4 style="color: #a78bfa;">📋 Step 4: Run in SUMO</h4>
            <p style="color: #e2e8f0;">Use netconvert to build network, then run simulation</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # What is ClickSUMO
    with st.expander("ℹ️ What is ClickSUMO?", expanded=False):
        st.markdown("""
        <p style="font-size: 1.1rem; font-weight: 500; color: #f8fafc; margin-bottom: 1.5rem; letter-spacing: -0.01em;">ClickSUMO is a web-based AI-assisted tool that makes SUMO traffic simulation accessible to everyone.</p>

        <p style="font-weight: 600; color: #8b5cf6; margin-top: 2rem; margin-bottom: 1rem; letter-spacing: 0.05em; text-transform: uppercase;">Key Features</p>
        <ul style="color: #cbd5e1; font-size: 1rem;">
            <li style="margin-bottom: 0.8rem;">🎯 <strong>No coding required</strong> - Visual interface for all tasks</li>
            <li style="margin-bottom: 0.8rem;">📦 <strong>Ready-to-use templates</strong> - Common network patterns included</li>
            <li style="margin-bottom: 0.8rem;">📥 <strong>Easy download</strong> - Get all files with one click</li>
            <li style="margin-bottom: 0.8rem;">🤖 <strong>AI-powered</strong> - Get help from our AI assistant</li>
        </ul>

        <p style="font-weight: 600; color: #6366f1; margin-top: 2rem; margin-bottom: 1rem; letter-spacing: 0.05em; text-transform: uppercase;">Who is it for?</p>
        <ul style="color: #cbd5e1; font-size: 1rem;">
            <li style="margin-bottom: 0.8rem;">🎓 Students learning traffic simulation</li>
            <li style="margin-bottom: 0.8rem;">🔬 Researchers who need quick prototypes</li>
            <li style="margin-bottom: 0.8rem;">🏢 Practitioners evaluating scenarios</li>
        </ul>
        """, unsafe_allow_html=True)


# =============================================================================
# NETWORK STUDIO
# =============================================================================

def show_network_studio():
    st.markdown('<h1>🛣️ Network Studio</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-weight: 500;">Create and configure your road network</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Templates", "✏️ Custom Editor", "🗺️ OSM Import"])
    
    # --- TEMPLATES TAB ---
    with tab1:
        st.markdown("### 🎨 Choose a Network Template")
        
        templates = list_templates()
        
        template_icons = {
            "4way": "🚦",
            "3way": "🔀",
            "roundabout": "🔄",
            "grid": "🏙️",
            "corridor": "🛤️",
            "highway": "🛣️"
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Select Template:**")
            selected_template = st.radio(
                "template",
                options=[t['key'] for t in templates],
                format_func=lambda x: f"{template_icons.get(x, '📍')} {[t['name'] for t in templates if t['key']==x][0]}",
                label_visibility="collapsed"
            )
        
        with col2:
            template_desc = {
                "4way": "Standard 4-way signalized intersection. Perfect for studying signal timing and queue dynamics.",
                "3way": "T-intersection (3-way). Common in residential areas and minor arterials.",
                "roundabout": "Modern roundabout with configurable arms. Great for comparing with signalized intersections.",
                "grid": "Grid network like downtown areas. Ideal for network-level analysis.",
                "corridor": "Arterial corridor with multiple signals. Perfect for signal coordination studies.",
                "highway": "Highway segment with on/off ramps. For freeway merge/diverge analysis."
            }
            
            st.info(f"ℹ️ {template_desc.get(selected_template, 'Select a template')}")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Configuration based on template
        st.markdown("### ⚙️ Configure Parameters")
        
        if selected_template == "4way":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**🛣️ Road Geometry**")
                arm_length = st.slider("Arm Length (m)", 100, 500, 200, help="Length of each approach")
                lanes = st.slider("Lanes per Direction", 1, 4, 2, help="Number of lanes")
            with col2:
                st.markdown("**🚗 Traffic Settings**")
                speed = st.slider("Speed Limit (km/h)", 30, 80, 50)
            with col3:
                st.markdown("**🚦 Signal Timing**")
                green_ns = st.slider("Green Time N-S (s)", 15, 60, 30)
                green_ew = st.slider("Green Time E-W (s)", 15, 60, 30)
                yellow = st.slider("Yellow Time (s)", 2, 5, 3)
            
            config = {
                "arm_length": arm_length,
                "lanes_per_arm": lanes,
                "speed_limit": speed,
                "green_time_ns": green_ns,
                "green_time_ew": green_ew,
                "yellow_time": yellow
            }
        
        elif selected_template == "grid":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**🏙️ Grid Size**")
                rows = st.slider("Rows", 2, 10, 3)
                cols = st.slider("Columns", 2, 10, 3)
            with col2:
                st.markdown("**🛣️ Block Settings**")
                block_length = st.slider("Block Length (m)", 100, 500, 200)
                lanes = st.slider("Lanes", 1, 4, 2)
            with col3:
                st.markdown("**🚦 Signals**")
                speed = st.slider("Speed Limit (km/h)", 30, 80, 50)
                signalized = st.checkbox("Signalized Intersections", True)
            
            config = {
                "rows": rows,
                "cols": cols,
                "block_length": block_length,
                "lanes": lanes,
                "speed_limit": speed,
                "signalized": signalized
            }
        
        elif selected_template == "corridor":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**🛤️ Corridor Layout**")
                num_int = st.slider("Number of Intersections", 2, 10, 5)
                spacing = st.slider("Spacing (m)", 200, 500, 300)
            with col2:
                st.markdown("**🛣️ Road Settings**")
                main_lanes = st.slider("Main Road Lanes", 2, 4, 3)
                cross_lanes = st.slider("Cross Street Lanes", 1, 3, 2)
            with col3:
                st.markdown("**🚗 Speed**")
                main_speed = st.slider("Main Road Speed (km/h)", 40, 80, 60)
                signalized = st.checkbox("Signalized", True)
            
            config = {
                "num_intersections": num_int,
                "spacing": spacing,
                "main_lanes": main_lanes,
                "cross_lanes": cross_lanes,
                "main_speed": main_speed,
                "signalized": signalized
            }
        
        elif selected_template == "roundabout":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**🔄 Roundabout Size**")
                num_arms = st.slider("Number of Arms", 3, 6, 4)
                radius = st.slider("Radius (m)", 15, 50, 30)
            with col2:
                st.markdown("**🛣️ Approach Roads**")
                arm_length = st.slider("Arm Length (m)", 100, 300, 200)
                lanes = st.slider("Lanes per Arm", 1, 2, 1)
            with col3:
                st.markdown("**🔄 Circulating**")
                rb_lanes = st.slider("Roundabout Lanes", 1, 3, 2)
                speed = st.slider("Speed Limit (km/h)", 20, 50, 30)
            
            config = {
                "num_arms": num_arms,
                "radius": radius,
                "arm_length": arm_length,
                "lanes_per_arm": lanes,
                "roundabout_lanes": rb_lanes,
                "speed_limit": speed
            }
        
        elif selected_template == "highway":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**🛣️ Highway Length**")
                length = st.slider("Length (m)", 1000, 5000, 2000)
                lanes = st.slider("Lanes", 2, 5, 3)
            with col2:
                st.markdown("**🚗 Speed**")
                speed = st.slider("Speed Limit (km/h)", 80, 130, 100)
            with col3:
                st.markdown("**🔀 Ramps**")
                num_ramps = st.slider("Number of Ramps", 1, 4, 2)
                ramp_lanes = st.slider("Ramp Lanes", 1, 2, 1)
            
            config = {
                "length": length,
                "lanes": lanes,
                "speed_limit": speed,
                "num_ramps": num_ramps,
                "ramp_lanes": ramp_lanes
            }
        
        elif selected_template == "3way":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🛣️ Road Geometry**")
                arm_length = st.slider("Arm Length (m)", 100, 500, 200)
                lanes = st.slider("Lanes per Arm", 1, 4, 2)
            with col2:
                st.markdown("**🚗 Settings**")
                speed = st.slider("Speed Limit (km/h)", 30, 80, 50)
                has_signal = st.checkbox("Has Traffic Signal", True)
            
            config = {
                "arm_length": arm_length,
                "lanes_per_arm": lanes,
                "speed_limit": speed,
                "has_signal": has_signal
            }
        
        else:
            config = {}
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_clicked = st.button("🔨 Generate Network", use_container_width=True, type="primary")
        
        if generate_clicked:
            with st.spinner("🔄 Generating network..."):
                try:
                    network = create_network(selected_template, **config)
                    
                    output_dir = "outputs"
                    os.makedirs(output_dir, exist_ok=True)
                    network.save_all(output_dir, "network")
                    
                    st.session_state.network = network
                    
                    files = [f for f in os.listdir(output_dir) if f.startswith("network.") and f.endswith(".xml")]
                    st.session_state.generated_files = files
                    
                    st.success("✅ Network generated successfully!")
                    
                    st.markdown("### 📥 Download Your Files")
                    
                    cols = st.columns(len(files))
                    for i, f in enumerate(files):
                        filepath = os.path.join(output_dir, f)
                        with open(filepath, 'r') as file:
                            file_content = file.read()
                        with cols[i]:
                            st.download_button(
                                label=f"⬇️ {f}",
                                data=file_content,
                                file_name=f,
                                mime="application/xml",
                                key=f"download_{f}",
                                use_container_width=True
                            )
                    
                    st.markdown("---")
                    
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for f in files:
                            filepath = os.path.join(output_dir, f)
                            zip_file.write(filepath, f)
                    zip_buffer.seek(0)
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="📦 Download ALL Files (ZIP)",
                            data=zip_buffer.getvalue(),
                            file_name="sumo_network.zip",
                            mime="application/zip",
                            key="download_all_zip",
                            use_container_width=True
                        )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # --- CUSTOM EDITOR TAB ---
    with tab2:
        st.markdown("### ✏️ Custom Network Editor")
        st.markdown('<p style="color: #94a3b8; font-weight: 500;">Build your network by adding nodes and edges manually</p>', unsafe_allow_html=True)
        
        if 'custom_nodes' not in st.session_state:
            st.session_state.custom_nodes = []
        if 'custom_edges' not in st.session_state:
            st.session_state.custom_edges = []
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📍 Add Nodes (Junctions)")
            
            node_col1, node_col2 = st.columns(2)
            with node_col1:
                node_id = st.text_input("Node ID", placeholder="e.g., n1", key="node_id")
                node_x = st.number_input("X Coordinate (m)", value=0.0, key="node_x")
            with node_col2:
                node_type = st.selectbox("Type", ["priority", "traffic_light", "right_before_left", "unregulated"], key="node_type")
                node_y = st.number_input("Y Coordinate (m)", value=0.0, key="node_y")
            
            if st.button("➕ Add Node", use_container_width=True):
                if node_id and not any(n['id'] == node_id for n in st.session_state.custom_nodes):
                    st.session_state.custom_nodes.append({
                        'id': node_id,
                        'x': node_x,
                        'y': node_y,
                        'type': node_type
                    })
                    st.success(f"✅ Node '{node_id}' added!")
                    st.rerun()
                else:
                    st.error("⚠️ Node ID already exists or is empty!")
            
            st.markdown("---")
            st.markdown("#### 🔗 Add Edges (Roads)")
            
            if len(st.session_state.custom_nodes) >= 2:
                node_ids = [n['id'] for n in st.session_state.custom_nodes]
                
                edge_col1, edge_col2 = st.columns(2)
                with edge_col1:
                    edge_id = st.text_input("Edge ID", placeholder="e.g., e1", key="edge_id")
                    from_node = st.selectbox("From Node", node_ids, key="from_node")
                    num_lanes = st.number_input("Number of Lanes", 1, 6, 2, key="num_lanes")
                with edge_col2:
                    edge_priority = st.number_input("Priority", 1, 10, 5, key="edge_priority")
                    to_node = st.selectbox("To Node", node_ids, key="to_node")
                    speed_limit = st.number_input("Speed Limit (m/s)", 5.0, 40.0, 13.89, key="speed_limit")
                
                if st.button("➕ Add Edge", use_container_width=True):
                    if edge_id and from_node != to_node and not any(e['id'] == edge_id for e in st.session_state.custom_edges):
                        st.session_state.custom_edges.append({
                            'id': edge_id,
                            'from': from_node,
                            'to': to_node,
                            'numLanes': num_lanes,
                            'speed': speed_limit,
                            'priority': edge_priority
                        })
                        st.success(f"✅ Edge '{edge_id}' added!")
                        st.rerun()
                    else:
                        st.error("⚠️ Invalid edge configuration!")
            else:
                st.info("ℹ️ Add at least 2 nodes first to create edges")
        
        with col2:
            st.markdown("#### 📊 Network Preview")
            
            if st.session_state.custom_nodes:
                st.markdown(f"**Nodes ({len(st.session_state.custom_nodes)}):**")
                for node in st.session_state.custom_nodes:
                    st.markdown(f"📍 **{node['id']}** - ({node['x']}, {node['y']}) - *{node['type']}*")
                    if st.button(f"🗑️", key=f"del_node_{node['id']}", help="Delete Node"):
                        st.session_state.custom_nodes = [n for n in st.session_state.custom_nodes if n['id'] != node['id']]
                        st.session_state.custom_edges = [e for e in st.session_state.custom_edges if e['from'] != node['id'] and e['to'] != node['id']]
                        st.rerun()
            
            if st.session_state.custom_edges:
                st.markdown(f"**Edges ({len(st.session_state.custom_edges)}):**")
                for edge in st.session_state.custom_edges:
                    st.markdown(f"🔗 **{edge['id']}**: {edge['from']} → {edge['to']} ({edge['numLanes']} lanes, {edge['speed']} m/s)")
                    if st.button(f"🗑️", key=f"del_edge_{edge['id']}", help="Delete Edge"):
                        st.session_state.custom_edges = [e for e in st.session_state.custom_edges if e['id'] != edge['id']]
                        st.rerun()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        if st.session_state.custom_nodes and st.session_state.custom_edges:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔨 Generate Custom Network", use_container_width=True, type="primary"):
                    with st.spinner("🔄 Generating custom network..."):
                        try:
                            output_dir = "outputs"
                            os.makedirs(output_dir, exist_ok=True)
                            
                            nodes_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<nodes>\n'
                            for node in st.session_state.custom_nodes:
                                # Escape user input to prevent XML injection
                                node_id = html.escape(str(node["id"]), quote=True)
                                node_type = html.escape(str(node["type"]), quote=True)
                                nodes_xml += f'    <node id="{node_id}" x="{node["x"]}" y="{node["y"]}" type="{node_type}"/>\n'
                            nodes_xml += '</nodes>'

                            edges_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<edges>\n'
                            for edge in st.session_state.custom_edges:
                                # Escape user input to prevent XML injection
                                edge_id = html.escape(str(edge["id"]), quote=True)
                                edge_from = html.escape(str(edge["from"]), quote=True)
                                edge_to = html.escape(str(edge["to"]), quote=True)
                                edges_xml += f'    <edge id="{edge_id}" from="{edge_from}" to="{edge_to}" numLanes="{edge["numLanes"]}" speed="{edge["speed"]}" priority="{edge["priority"]}"/>\n'
                            edges_xml += '</edges>'
                            
                            with open(os.path.join(output_dir, "custom_network.nod.xml"), "w") as f:
                                f.write(nodes_xml)
                            with open(os.path.join(output_dir, "custom_network.edg.xml"), "w") as f:
                                f.write(edges_xml)
                            
                            st.success("✅ Custom network generated successfully!")
                            
                            st.markdown("### 📥 Download Your Files")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button("⬇️ Nodes File", nodes_xml, "custom_network.nod.xml", "application/xml")
                            with col2:
                                st.download_button("⬇️ Edges File", edges_xml, "custom_network.edg.xml", "application/xml")
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    # --- OSM IMPORT TAB ---
    with tab3:
        st.markdown("### 🗺️ OpenStreetMap Import")
        st.markdown('<p style="color: #94a3b8; font-weight: 500;">Import real-world road networks from OpenStreetMap</p>', unsafe_allow_html=True)
        
        osm_tab1, osm_tab2, osm_tab3 = st.tabs(["🧙‍♂️ osmWebWizard (Easy)", "📍 Manual Coordinates", "📋 Step-by-Step Guide"])
        
        # --- osmWebWizard TAB ---
        with osm_tab1:
            st.markdown("""
            <div class='info-box'>
            <h4 style="color: #a78bfa;">🧙‍♂️ SUMO's osmWebWizard - The Easiest Way!</h4>
            <p style="color: #e2e8f0;">osmWebWizard is SUMO's official tool for importing OSM networks with a visual map interface.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### ✨ What is osmWebWizard?")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("""
                <p style='font-weight: 600; color: #cbd5e1; margin-bottom: 0.8rem;'>Features:</p>
                <ul style='color: #94a3b8;'>
                    <li style='margin: 0.5rem 0;'>🗺️ <strong>Interactive Map</strong></li>
                    <li style='margin: 0.5rem 0;'>⚡ <strong>One-Click Import</strong></li>
                    <li style='margin: 0.5rem 0;'>🚗 <strong>Traffic Generation</strong></li>
                    <li style='margin: 0.5rem 0;'>🎮 <strong>Instant Preview</strong></li>
                    <li style='margin: 0.5rem 0;'>⚙️ <strong>Smart Settings</strong></li>
                </ul>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <p style='font-weight: 600; color: #cbd5e1; margin-bottom: 0.8rem;'>Perfect For:</p>
                <ul style='color: #94a3b8;'>
                    <li style='margin: 0.5rem 0;'>🎓 <strong>Beginners</strong></li>
                    <li style='margin: 0.5rem 0;'>⚡ <strong>Quick Tests</strong></li>
                    <li style='margin: 0.5rem 0;'>🏙️ <strong>City Networks</strong></li>
                    <li style='margin: 0.5rem 0;'>🔬 <strong>Research</strong></li>
                    <li style='margin: 0.5rem 0;'>📚 <strong>Teaching</strong></li>
                </ul>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            st.markdown("### 🚀 Launch osmWebWizard")
            
            st.markdown("""
            <div class='warning-box'>
            <h4 style="color: #fcd34d;">⚠️ Requirements:</h4>
            <p style="color: #e2e8f0;">You need SUMO installed on your system. osmWebWizard comes bundled with SUMO.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🪟 Windows Users")
                st.markdown("**Method 1: Command Line**")
                
                windows_cmd = """cd %SUMO_HOME%\\tools
python osmWebWizard.py"""
                
                st.code(windows_cmd, language="bash")
                
                st.markdown("**Method 2: Start Menu**")
                st.markdown("Search for \"osmWebWizard\" in Start Menu")
            
            with col2:
                st.markdown("#### 🐧 Linux/Mac Users")
                st.markdown("**Terminal Command:**")
                
                linux_cmd = """cd $SUMO_HOME/tools
python3 osmWebWizard.py

# Or if SUMO tools are in PATH:
osmWebWizard.py"""
                
                st.code(linux_cmd, language="bash")
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            st.markdown("### 📖 How to Use osmWebWizard")
            
            step_col1, step_col2 = st.columns([1, 1])
            
            with step_col1:
                st.markdown("""
                <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="color: #8b5cf6;">1️⃣ Launch the Tool</h4>
                <p style='color: #cbd5e1; font-size: 0.9rem;'>Run the command above - your web browser will open automatically</p>
                </div>
                
                <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="color: #8b5cf6;">2️⃣ Select Area</h4>
                <ul style='font-size: 0.9rem; color: #94a3b8;'>
                    <li>Search for a city or place</li>
                    <li>Drag to select rectangular area</li>
                    <li>Adjust size as needed</li>
                </ul>
                </div>
                
                <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="color: #8b5cf6;">3️⃣ Configure Options</h4>
                <ul style='font-size: 0.9rem; color: #94a3b8;'>
                    <li><strong>Duration:</strong> Simulation time</li>
                    <li><strong>Traffic:</strong> Generate random traffic</li>
                    <li><strong>Demand:</strong> Vehicles per hour</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with step_col2:
                st.markdown("""
                <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="color: #8b5cf6;">4️⃣ Generate Network</h4>
                <p style='color: #cbd5e1; font-size: 0.9rem;'>Click "Generate Scenario" - osmWebWizard will:</p>
                <ul style='font-size: 0.9rem; color: #94a3b8;'>
                    <li>Download OSM data</li>
                    <li>Convert to SUMO network</li>
                    <li>Generate traffic</li>
                    <li>Save all files</li>
                </ul>
                </div>
                
                <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="color: #8b5cf6;">5️⃣ Launch Simulation</h4>
                <p style='color: #cbd5e1; font-size: 0.9rem;'>Click "Run in SUMO-GUI" to see your simulation in action!</p>
                </div>
                
                <div class="success-box">
                <h4 style="color: #10b981;">✅ Done!</h4>
                <p style='color: #cbd5e1; font-size: 0.9rem;'>All files are saved in a timestamped folder in your current directory</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            st.markdown("### 💡 Pro Tips")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <p style='font-weight: 600; color: #cbd5e1; margin-bottom: 0.8rem;'>📏 Area Selection:</p>
                <ul style='font-size: 0.9rem; color: #94a3b8;'>
                    <li style='margin: 0.4rem 0;'>Start small (1-2 km²)</li>
                    <li style='margin: 0.4rem 0;'>Larger = slower processing</li>
                    <li style='margin: 0.4rem 0;'>Focus on area of interest</li>
                </ul>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <p style='font-weight: 600; color: #cbd5e1; margin-bottom: 0.8rem;'>⚡ Performance:</p>
                <ul style='font-size: 0.9rem; color: #94a3b8;'>
                    <li style='margin: 0.4rem 0;'>Reduce duration for faster runs</li>
                    <li style='margin: 0.4rem 0;'>Lower traffic density for big areas</li>
                    <li style='margin: 0.4rem 0;'>Use "through traffic" sparingly</li>
                </ul>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <p style='font-weight: 600; color: #cbd5e1; margin-bottom: 0.8rem;'>📁 Output Files:</p>
                <ul style='font-size: 0.9rem; color: #94a3b8;'>
                    <li style='margin: 0.4rem 0;'>Find in dated folder</li>
                    <li style='margin: 0.4rem 0;'>Contains .net.xml, .rou.xml</li>
                    <li style='margin: 0.4rem 0;'>Copy to ClickSUMO outputs/</li>
                </ul>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### 🎯 Quick Actions")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.link_button("📖 osmWebWizard Docs", "https://sumo.dlr.de/docs/Tools/Import/OSM.html#osmwebwizardpy", use_container_width=True)
                with col_b:
                    st.link_button("💾 Download SUMO", "https://www.eclipse.org/sumo/", use_container_width=True)
        
        # --- MANUAL COORDINATES TAB ---
        with osm_tab2:
            st.markdown("#### 📍 Define Area by Coordinates")
            
            import_method = st.radio("Coordinate Method:", ["Bounding Box", "Place Name"], horizontal=True, key="coord_method")
        
            if import_method == "Bounding Box":
                st.markdown("##### 📐 Enter Bounding Box Coordinates")
                col1, col2 = st.columns(2)
                with col1:
                    min_lat = st.number_input("Min Latitude", value=40.7000, format="%.6f", help="Bottom-left corner")
                    min_lon = st.number_input("Min Longitude", value=-74.0200, format="%.6f", help="Bottom-left corner")
                with col2:
                    max_lat = st.number_input("Max Latitude", value=40.7100, format="%.6f", help="Top-right corner")
                    max_lon = st.number_input("Max Longitude", value=-74.0100, format="%.6f", help="Top-right corner")
                
                st.info(f"📐 Area: {abs(max_lat - min_lat):.4f}° × {abs(max_lon - min_lon):.4f}° (~{abs(max_lat - min_lat) * 111:.2f} km × {abs(max_lon - min_lon) * 111:.2f} km)")
            
            else:
                st.markdown("##### 🏙️ Search by Place Name")
                place_name = st.text_input("Place Name", placeholder="e.g., Manhattan, New York, USA", help="Enter city, district, or landmark name")
                radius = st.slider("Radius (km)", 0.5, 10.0, 2.0, 0.5, help="Area around the place to import")
            
            st.markdown("---")
            st.markdown("##### 🛣️ Road Type Filter")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                highway = st.checkbox("🛣️ Highways", True)
                primary = st.checkbox("🚗 Primary Roads", True)
                secondary = st.checkbox("🚙 Secondary Roads", True)
            with col2:
                residential = st.checkbox("🏘️ Residential", True)
                service = st.checkbox("🅿️ Service Roads", False)
                footway = st.checkbox("🚶 Footways", False)
            with col3:
                cycleway = st.checkbox("🚴 Cycleways", False)
                motorway = st.checkbox("🏎️ Motorways", True)
                trunk = st.checkbox("🛤️ Trunk Roads", True)
            
            st.markdown("---")
            st.markdown("##### ⚙️ Import Options")
            
            col1, col2 = st.columns(2)
            with col1:
                import_tls = st.checkbox("Import Traffic Lights", True, help="Include existing traffic signals")
                simplify = st.checkbox("Simplify Network", True, help="Merge simple edges")
            with col2:
                remove_edges = st.checkbox("Remove Disconnected Edges", True)
                guess_tls = st.checkbox("Guess Missing Traffic Lights", False)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🌍 Generate Import Script", use_container_width=True, type="primary", key="gen_script"):
                    try:
                        road_types = []
                        if highway: road_types.append('highway')
                        if primary: road_types.append('primary')
                        if secondary: road_types.append('secondary')
                        if residential: road_types.append('residential')
                        if service: road_types.append('service')
                        if footway: road_types.append('footway')
                        if cycleway: road_types.append('cycleway')
                        if motorway: road_types.append('motorway')
                        if trunk: road_types.append('trunk')
                        
                        if import_method == "Bounding Box":
                            bbox_str = f"{min_lat},{min_lon},{max_lat},{max_lon}"
                            query_info = f"Bounding Box: ({min_lat:.4f}, {min_lon:.4f}) to ({max_lat:.4f}, {max_lon:.4f})"
                        else:
                            bbox_str = f"place:{place_name}"
                            query_info = f"Place: {place_name} (Radius: {radius} km)"
                        
                        netconvert_cmd = f"""netconvert --osm-files map.osm \\
    --output-file osm_network.net.xml \\
    --geometry.remove \\
    --ramps.guess \\
    --junctions.join \\
    --tls.guess-signals {str(guess_tls).lower()} \\
    --tls.discard-loaded {str(not import_tls).lower()} \\
    --remove-edges.isolated {str(remove_edges).lower()}"""
                        
                        st.success("✅ Configuration ready!")
                        
                        st.markdown("### 📋 Import Instructions")
                        st.markdown(f"**Query:** {query_info}")
                        
                        st.markdown("**1️⃣ Download OSM Data:**")
                        st.markdown(f"- Visit [OpenStreetMap Export](https://www.openstreetmap.org/export)")
                        st.markdown(f"- Download as `map.osm`")
                        
                        st.markdown("**2️⃣ Run netconvert:**")
                        st.code(netconvert_cmd, language="bash")
                        
                        script_content = f"""#!/bin/bash
# ClickSUMO - OSM Import Script
# Created by Mahbub Hassan's ClickSUMO Tool
# Query: {query_info}
# Road Types: {', '.join(road_types)}

{netconvert_cmd}
"""
                        st.download_button(
                            "📥 Download Import Script",
                            script_content,
                            "osm_import.sh",
                            "text/plain",
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        # --- STEP-BY-STEP GUIDE TAB ---
        with osm_tab3:
            st.markdown("#### 📚 Complete OSM Import Guide")
            
            st.markdown("""
            <div class='info-box'>
            <h4 style="color: #a78bfa;">📖 Comprehensive Tutorial</h4>
            <p style="color: #e2e8f0;">Learn all methods to import OpenStreetMap data into SUMO</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🔄 Import Methods Comparison")
            
            methods_data = {
                "Method": ["osmWebWizard", "netconvert", "ClickSUMO Script"],
                "Difficulty": ["⭐ Easy", "⭐⭐⭐ Advanced", "⭐⭐ Medium"],
                "Speed": ["Fast", "Fast", "Fast"],
                "GUI": ["✅ Yes", "❌ No", "❌ No"],
                "Traffic Gen": ["✅ Yes", "❌ No", "❌ No"],
                "Best For": ["Quick start", "Custom needs", "Automation"]
            }
            
            import pandas as pd
            df_methods = pd.DataFrame(methods_data)
            st.dataframe(df_methods, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("### 📍 Where to Find Coordinates")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="color: #06b6d4;">Option 1: OpenStreetMap.org</h4>
                <ol style='font-size: 0.9rem; color: #94a3b8;'>
                    <li>Go to openstreetmap.org</li>
                    <li>Navigate to desired area</li>
                    <li>Click "Export" button</li>
                    <li>See bounding box coordinates</li>
                </ol>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="color: #06b6d4;">Option 2: bboxfinder.com</h4>
                <ol style='font-size: 0.9rem; color: #94a3b8;'>
                    <li>Visit bboxfinder.com</li>
                    <li>Draw rectangle on map</li>
                    <li>Copy coordinates</li>
                    <li>Paste in ClickSUMO</li>
                </ol>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🔗 Useful Resources")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.link_button("🗺️ OpenStreetMap", "https://www.openstreetmap.org/export", use_container_width=True)
            with col2:
                st.link_button("📦 bbox Finder", "http://bboxfinder.com/", use_container_width=True)
            with col3:
                st.link_button("📖 SUMO Wiki", "https://sumo.dlr.de/docs/Networks/Import/OpenStreetMap.html", use_container_width=True)


# =============================================================================
# DEMAND GENERATOR
# =============================================================================

def show_demand_generator():
    st.markdown('<h1>🚗 Demand Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-weight: 500;">Define vehicles and traffic demand</p>', unsafe_allow_html=True)
    
    if not st.session_state.network:
        st.warning("⚠️ Please generate a network first in Network Studio!")
        st.info("👈 Go to **Network Studio** in the sidebar to create a network.")
        return
    
    tab1, tab2, tab3 = st.tabs(["🚙 Vehicle Types", "🔄 Traffic Flows", "📥 Generate Files"])
    
    # --- VEHICLE TYPES TAB ---
    with tab1:
        st.markdown("### 🚙 Define Vehicle Types")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.expander("➕ Add New Vehicle Type", expanded=True):
                c1, c2 = st.columns(2)
                
                with c1:
                    vtype_id = st.text_input("Type ID", "car", key="vtype_id")
                    vclass = st.selectbox("Vehicle Class", 
                        ["passenger", "truck", "bus", "motorcycle", "bicycle", "pedestrian"],
                        key="vclass")
                    length = st.number_input("Length (m)", 1.0, 20.0, 5.0, key="length")
                    max_speed = st.number_input("Max Speed (km/h)", 20.0, 250.0, 180.0, key="max_speed")
                
                with c2:
                    accel = st.number_input("Acceleration (m/s²)", 0.5, 5.0, 2.6, key="accel")
                    decel = st.number_input("Deceleration (m/s²)", 1.0, 10.0, 4.5, key="decel")
                    sigma = st.slider("Driver Imperfection", 0.0, 1.0, 0.5, key="sigma")
                    color = st.color_picker("Color", "#FF0000", key="color")
                
                if st.button("➕ Add Vehicle Type", key="add_vtype"):
                    vtype = {
                        "id": vtype_id,
                        "vclass": vclass,
                        "length": length,
                        "max_speed": kmh_to_ms(max_speed),
                        "accel": accel,
                        "decel": decel,
                        "sigma": sigma,
                        "color": color
                    }
                    st.session_state.vehicle_types.append(vtype)
                    st.success(f"✅ Added: {vtype_id}")
                    st.rerun()
        
        with col2:
            st.markdown("### 📋 Current Types")
            if st.session_state.vehicle_types:
                for i, vt in enumerate(st.session_state.vehicle_types):
                    st.markdown(f"""
                    <span style="color:{vt['color']}; font-size: 1.5rem; margin-right: 8px;">●</span>
                    <strong>{vt['id']}</strong> ({vt['vclass']})
                    """, unsafe_allow_html=True)
                    if st.button("🗑️ Remove", key=f"del_vtype_{i}"):
                        st.session_state.vehicle_types.pop(i)
                        st.rerun()
            else:
                st.info("No vehicle types defined yet")
    
    # --- TRAFFIC FLOWS TAB ---
    with tab2:
        st.markdown("### 🔄 Define Traffic Flows")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.expander("➕ Add New Flow", expanded=True):
                c1, c2 = st.columns(2)
                
                with c1:
                    flow_id = st.text_input("Flow ID", "flow_1", key="flow_id")
                    from_edge = st.text_input("From Edge", "N2C", key="from_edge",
                        help="Edge ID where vehicles enter")
                    to_edge = st.text_input("To Edge", "C2S", key="to_edge",
                        help="Edge ID where vehicles exit")
                
                with c2:
                    vtype_options = ["DEFAULT_VEHTYPE"] + [vt['id'] for vt in st.session_state.vehicle_types]
                    vtype = st.selectbox("Vehicle Type", vtype_options, key="flow_vtype")
                    begin = st.number_input("Begin Time (s)", 0, 86400, 0, key="begin")
                    end = st.number_input("End Time (s)", 0, 86400, 3600, key="end")
                    vph = st.number_input("Vehicles per Hour", 10, 5000, 500, key="vph")
                
                if st.button("➕ Add Flow", key="add_flow"):
                    flow = {
                        "id": flow_id,
                        "from_edge": from_edge,
                        "to_edge": to_edge,
                        "vtype": vtype,
                        "begin": begin,
                        "end": end,
                        "vph": vph
                    }
                    st.session_state.flows.append(flow)
                    st.success(f"✅ Added: {flow_id}")
                    st.rerun()
        
        with col2:
            st.markdown("### 📋 Current Flows")
            if st.session_state.flows:
                for i, fl in enumerate(st.session_state.flows):
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 8px;">
                        <strong>{fl['id']}</strong><br>
                        {fl['from_edge']} → {fl['to_edge']}<br>
                        {fl['vph']} veh/h
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("🗑️ Remove", key=f"del_flow_{i}"):
                        st.session_state.flows.pop(i)
                        st.rerun()
            else:
                st.info("No flows defined yet")
    
    # --- GENERATE FILES TAB ---
    with tab3:
        st.markdown("### 📥 Generate Route File")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Vehicle Types", len(st.session_state.vehicle_types))
        with col2:
            st.metric("Traffic Flows", len(st.session_state.flows))
        with col3:
            total_vph = sum(fl['vph'] for fl in st.session_state.flows)
            st.metric("Total Vehicles/Hour", total_vph)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔨 Generate Route File", type="primary", use_container_width=True):
                try:
                    with st.spinner("Generating..."):
                        os.makedirs("outputs", exist_ok=True)
                        
                        routes = RouteGenerator()
                        
                        for vt in st.session_state.vehicle_types:
                            routes.add_vehicle_type(VehicleType(
                                id=vt['id'],
                                vclass=vt['vclass'],
                                length=vt['length'],
                                max_speed=vt['max_speed'],
                                accel=vt['accel'],
                                decel=vt['decel'],
                                sigma=vt['sigma'],
                                color=vt['color']
                            ))
                        
                        for fl in st.session_state.flows:
                            routes.add_flow(Flow(
                                id=fl['id'],
                                from_edge=fl['from_edge'],
                                to_edge=fl['to_edge'],
                                vtype=fl['vtype'],
                                begin=fl['begin'],
                                end=fl['end'],
                                vehs_per_hour=fl['vph']
                            ))
                        
                        output_path = "outputs/network.rou.xml"
                        routes.save(output_path)
                        
                        st.session_state.routes = routes
                        
                        if "network.rou.xml" not in st.session_state.generated_files:
                            st.session_state.generated_files.append("network.rou.xml")
                        
                        st.success("✅ Route file generated!")
                        
                        with open(output_path, 'r') as f:
                            route_content = f.read()
                        
                        st.download_button(
                            label="⬇️ Download network.rou.xml",
                            data=route_content,
                            file_name="network.rou.xml",
                            mime="application/xml",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Error generating route file: {str(e)}")


# =============================================================================
# OUTPUT ANALYZER
# =============================================================================

def show_output_analyzer():
    st.markdown('<h1>📊 Output Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-weight: 500;">Analyze simulation results and generate reports</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Parse", "📈 Visualizations", "🎨 Advanced Charts", "📋 Export Report"])
    
    # --- UPLOAD TAB ---
    with tab1:
        st.markdown("### 📤 Upload SUMO Output Files")
        st.markdown('<p style="color: #94a3b8;">Support for multiple SUMO output formats</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 Core Output Files")
            
            tripinfo_file = st.file_uploader("Upload tripinfo.xml", type=['xml'], key="tripinfo",
                                            help="Contains vehicle trip information (duration, waiting time, etc.)")
            
            if tripinfo_file:
                try:
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(tripinfo_file)
                    root = tree.getroot()
                    
                    trips = []
                    for tripinfo in root.findall('tripinfo'):
                        trip_data = {
                            'id': tripinfo.get('id'),
                            'depart': float(tripinfo.get('depart', 0)),
                            'arrival': float(tripinfo.get('arrival', 0)),
                            'duration': float(tripinfo.get('duration', 0)),
                            'waitingTime': float(tripinfo.get('waitingTime', 0)),
                            'timeLoss': float(tripinfo.get('timeLoss', 0)),
                            'routeLength': float(tripinfo.get('routeLength', 0)),
                            'vType': tripinfo.get('vType', 'unknown')
                        }
                        trips.append(trip_data)
                    
                    st.session_state.trips_data = trips
                    st.success(f"✅ Loaded {len(trips)} trips")
                    
                    import pandas as pd
                    df = pd.DataFrame(trips)
                    st.dataframe(df.head(10), use_container_width=True)
                
                except Exception as e:
                    st.error(f"❌ Error parsing file: {str(e)}")
            
            st.markdown("---")
            summary_file = st.file_uploader("Upload summary.xml", type=['xml'], key="summary",
                                           help="Contains step-by-step simulation statistics")
            
            if summary_file:
                try:
                    tree = ET.parse(summary_file)
                    root = tree.getroot()
                    
                    summary_data = []
                    for step in root.findall('step'):
                        step_data = {
                            'time': float(step.get('time', 0)),
                            'loaded': int(step.get('loaded', 0)),
                            'inserted': int(step.get('inserted', 0)),
                            'running': int(step.get('running', 0)),
                            'waiting': int(step.get('waiting', 0)),
                            'ended': int(step.get('ended', 0)),
                            'meanSpeed': float(step.get('meanSpeed', 0)),
                            'meanWaitingTime': float(step.get('meanWaitingTime', 0))
                        }
                        summary_data.append(step_data)
                    
                    st.session_state.summary_data = summary_data
                    st.success(f"✅ Loaded {len(summary_data)} time steps")
                
                except Exception as e:
                    st.error(f"❌ Error parsing file: {str(e)}")
        
        with col2:
            st.markdown("#### 🌍 Environmental Data")
            
            emissions_file = st.file_uploader("Upload emissions.xml", type=['xml'], key="emissions",
                                             help="Contains vehicle emissions data (CO2, NOx, etc.)")
            
            if emissions_file:
                try:
                    tree = ET.parse(emissions_file)
                    root = tree.getroot()
                    
                    emissions = []
                    for vehicle in root.findall('.//vehicle'):
                        emission_data = {
                            'id': vehicle.get('id'),
                            'time': float(vehicle.get('time', 0)),
                            'CO2': float(vehicle.get('CO2', 0)),
                            'CO': float(vehicle.get('CO', 0)),
                            'HC': float(vehicle.get('HC', 0)),
                            'NOx': float(vehicle.get('NOx', 0)),
                            'PMx': float(vehicle.get('PMx', 0)),
                            'fuel': float(vehicle.get('fuel', 0)),
                            'electricity': float(vehicle.get('electricity', 0))
                        }
                        emissions.append(emission_data)
                    
                    st.session_state.emissions_data = emissions
                    st.success(f"✅ Loaded emissions for {len(emissions)} records")
                
                except Exception as e:
                    st.error(f"❌ Error parsing file: {str(e)}")
            
            st.markdown("---")
            edge_file = st.file_uploader("Upload edgedata.xml", type=['xml'], key="edgedata",
                                        help="Contains edge-level statistics (occupancy, speed, flow)")
            
            if edge_file:
                try:
                    tree = ET.parse(edge_file)
                    root = tree.getroot()
                    
                    edge_data = []
                    for interval in root.findall('.//interval'):
                        interval_time = float(interval.get('begin', 0))
                        for edge in interval.findall('edge'):
                            edge_info = {
                                'time': interval_time,
                                'id': edge.get('id'),
                                'sampledSeconds': float(edge.get('sampledSeconds', 0)),
                                'density': float(edge.get('density', 0)),
                                'occupancy': float(edge.get('occupancy', 0)),
                                'speed': float(edge.get('speed', 0)),
                                'traveltime': float(edge.get('traveltime', 0))
                            }
                            edge_data.append(edge_info)
                    
                    st.session_state.edge_data = edge_data
                    st.success(f"✅ Loaded {len(edge_data)} edge records")
                
                except Exception as e:
                    st.error(f"❌ Error parsing file: {str(e)}")
    
    # --- VISUALIZATION TAB ---
    with tab2:
        st.markdown("### 📈 Interactive Visualizations")
        
        if 'trips_data' not in st.session_state or not st.session_state.trips_data:
            st.info("📤 Please upload a tripinfo.xml file in Upload tab first")
        else:
            import pandas as pd
            import plotly.express as px
            import plotly.graph_objects as go
            
            df = pd.DataFrame(st.session_state.trips_data)
            
            # KPI Summary
            st.markdown("#### 📊 Key Performance Indicators")
            col1, col2, col3, col4 = st.columns(4)
            
            col1.metric("Total Vehicles", len(df))
            col2.metric("Avg Duration", f"{df['duration'].mean():.1f}s")
            col3.metric("Avg Waiting Time", f"{df['waitingTime'].mean():.1f}s")
            col4.metric("Avg Time Loss", f"{df['timeLoss'].mean():.1f}s")
            
            st.markdown("---")
            
            # Travel Time Distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🕐 Travel Time Distribution")
                fig_duration = px.histogram(df, x='duration', nbins=30,
                                           title="Trip Duration Distribution",
                                           labels={'duration': 'Duration (s)', 'count': 'Number of Vehicles'},
                                           color_discrete_sequence=['#8b5cf6'])
                fig_duration.update_layout(showlegend=False)
                st.plotly_chart(fig_duration, use_container_width=True)
            
            with col2:
                st.markdown("#### ⏱️ Waiting Time Distribution")
                fig_waiting = px.histogram(df, x='waitingTime', nbins=30,
                                          title="Waiting Time Distribution",
                                          labels={'waitingTime': 'Waiting Time (s)', 'count': 'Number of Vehicles'},
                                          color_discrete_sequence=['#06b6d4'])
                fig_waiting.update_layout(showlegend=False)
                st.plotly_chart(fig_waiting, use_container_width=True)
            
            # Time Loss Analysis
            st.markdown("#### 📉 Time Loss Analysis")
            fig_timeloss = px.box(df, y='timeLoss', 
                                 title="Time Loss Distribution (Box Plot)",
                                 labels={'timeLoss': 'Time Loss (s)'},
                                 color_discrete_sequence=['#6366f1'])
            st.plotly_chart(fig_timeloss, use_container_width=True)
            
            # Departure vs Arrival Timeline
            st.markdown("#### 🚦 Traffic Timeline")
            fig_timeline = go.Figure()
            fig_timeline.add_trace(go.Scatter(x=df['depart'], y=df.index, 
                                             mode='markers', name='Departure',
                                             marker=dict(color='#8b5cf6', size=5)))
            fig_timeline.add_trace(go.Scatter(x=df['arrival'], y=df.index,
                                             mode='markers', name='Arrival',
                                             marker=dict(color='#6366f1', size=5)))
            fig_timeline.update_layout(title="Vehicle Departures and Arrivals",
                                      xaxis_title="Time (s)",
                                      yaxis_title="Vehicle Index",
                                      height=400)
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Vehicle Type Analysis
            if 'vType' in df.columns:
                st.markdown("#### 🚗 Performance by Vehicle Type")
                vtype_stats = df.groupby('vType').agg({
                    'duration': 'mean',
                    'waitingTime': 'mean',
                    'timeLoss': 'mean'
                }).reset_index()
                
                fig_vtype = px.bar(vtype_stats, x='vType', y=['duration', 'waitingTime', 'timeLoss'],
                                  title="Average Metrics by Vehicle Type",
                                  labels={'value': 'Time (s)', 'variable': 'Metric'},
                                  barmode='group')
                st.plotly_chart(fig_vtype, use_container_width=True)
            
            # Emissions Visualization (if available)
            if 'emissions_data' in st.session_state and st.session_state.emissions_data:
                st.markdown("---")
                st.markdown("#### 🌍 Emissions Analysis")
                
                df_emissions = pd.DataFrame(st.session_state.emissions_data)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total CO2", f"{df_emissions['CO2'].sum():.2f} mg")
                col2.metric("Total NOx", f"{df_emissions['NOx'].sum():.2f} mg")
                col3.metric("Total Fuel", f"{df_emissions['fuel'].sum():.2f} ml")
                
                emission_totals = {
                    'CO2': df_emissions['CO2'].sum(),
                    'CO': df_emissions['CO'].sum(),
                    'NOx': df_emissions['NOx'].sum(),
                    'PMx': df_emissions['PMx'].sum()
                }
                
                fig_emissions = px.bar(x=list(emission_totals.keys()), y=list(emission_totals.values()),
                                      title="Total Emissions by Type",
                                      labels={'x': 'Emission Type', 'y': 'Amount (mg)'},
                                      color=list(emission_totals.keys()),
                                      color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig_emissions, use_container_width=True)
    
    # --- ADVANCED CHARTS TAB ---
    with tab3:
        st.markdown("### 🎨 Advanced Visualizations")
        st.markdown('<p style="color: #94a3b8; font-weight: 500;">Publication-ready charts and detailed analysis</p>', unsafe_allow_html=True)
        
        if 'trips_data' not in st.session_state or not st.session_state.trips_data:
            st.info("📤 Please upload tripinfo.xml file first")
        else:
            df = pd.DataFrame(st.session_state.trips_data)
            
            # Heatmap - Time vs Vehicle Type Performance
            st.markdown("#### 🔥 Performance Heatmap")
            if 'vType' in df.columns:
                # Create time bins
                df['hour'] = (df['depart'] // 3600).astype(int)
                heatmap_data = df.pivot_table(values='duration', index='vType', columns='hour', aggfunc='mean')
                
                fig_heatmap = px.imshow(heatmap_data,
                                       labels=dict(x="Hour", y="Vehicle Type", color="Avg Duration (s)"),
                                       title="Average Trip Duration by Vehicle Type and Hour",
                                       color_continuous_scale='Viridis')
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Violin plot for distribution comparison
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🎻 Duration Distribution (Violin Plot)")
                fig_violin = px.violin(df, y='duration', box=True, points='all',
                                      title="Trip Duration Detailed Distribution",
                                      color_discrete_sequence=['#8b5cf6'])
                st.plotly_chart(fig_violin, use_container_width=True)
            
            with col2:
                st.markdown("#### 📦 Time Loss by Vehicle Type")
                if 'vType' in df.columns:
                    fig_box_vtype = px.box(df, x='vType', y='timeLoss',
                                          title="Time Loss Distribution by Vehicle Type",
                                          color='vType')
                    st.plotly_chart(fig_box_vtype, use_container_width=True)
            
            # 3D Scatter Plot
            if 'routeLength' in df.columns:
                st.markdown("#### 🌐 3D Performance Analysis")
                fig_3d = px.scatter_3d(df, x='routeLength', y='duration', z='waitingTime',
                                      color='timeLoss',
                                      title="3D: Route Length vs Duration vs Waiting Time",
                                      labels={'routeLength': 'Route Length (m)', 
                                             'duration': 'Duration (s)',
                                             'waitingTime': 'Waiting Time (s)'},
                                      color_continuous_scale='Plasma')
                st.plotly_chart(fig_3d, use_container_width=True)
            
            # Summary statistics with time series
            if 'summary_data' in st.session_state and st.session_state.summary_data:
                st.markdown("---")
                st.markdown("#### 📈 Network Performance Over Time")
                
                df_summary = pd.DataFrame(st.session_state.summary_data)
                
                # Multi-line chart
                fig_network = go.Figure()
                fig_network.add_trace(go.Scatter(x=df_summary['time'], y=df_summary['running'],
                                                mode='lines', name='Running Vehicles',
                                                line=dict(color='#8b5cf6', width=3)))
                fig_network.add_trace(go.Scatter(x=df_summary['time'], y=df_summary['waiting'],
                                                mode='lines', name='Waiting Vehicles',
                                                line=dict(color='#06b6d4', width=3)))
                fig_network.add_trace(go.Scatter(x=df_summary['time'], y=df_summary['meanSpeed'],
                                                mode='lines', name='Mean Speed (m/s)', yaxis='y2',
                                                line=dict(color='#6366f1', width=3, dash='dash')))
                
                fig_network.update_layout(
                    title="Network Dynamics Over Time",
                    xaxis_title="Time (s)",
                    yaxis_title="Number of Vehicles",
                    yaxis2=dict(title="Speed (m/s)", overlaying='y', side='right'),
                    height=500,
                    hovermode='x unified'
                )
                st.plotly_chart(fig_network, use_container_width=True)
                
                # Congestion Analysis
                st.markdown("#### 🚦 Congestion Analysis")
                df_summary['congestion_index'] = (df_summary['waiting'] / (df_summary['running'] + 1)) * 100
                
                fig_congestion = px.area(df_summary, x='time', y='congestion_index',
                                        title="Congestion Index Over Time (%)",
                                        labels={'time': 'Time (s)', 'congestion_index': 'Congestion (%)'},
                                        color_discrete_sequence=['#06b6d4'])
                st.plotly_chart(fig_congestion, use_container_width=True)
            
            # Edge performance heatmap
            if 'edge_data' in st.session_state and st.session_state.edge_data:
                st.markdown("---")
                st.markdown("#### 🛣️ Edge Performance Analysis")
                
                df_edge = pd.DataFrame(st.session_state.edge_data)
                
                col1, col2 = st.columns(2)
                with col1:
                    # Speed heatmap by edge
                    edge_speed = df_edge.pivot_table(values='speed', index='id', columns='time', aggfunc='mean')
                    fig_edge_speed = px.imshow(edge_speed,
                                              labels=dict(x="Time", y="Edge ID", color="Speed (m/s)"),
                                              title="Edge Speed Heatmap",
                                              color_continuous_scale='Turbo')
                    st.plotly_chart(fig_edge_speed, use_container_width=True)
                
                with col2:
                    # Occupancy heatmap
                    edge_occ = df_edge.pivot_table(values='occupancy', index='id', columns='time', aggfunc='mean')
                    fig_edge_occ = px.imshow(edge_occ,
                                            labels=dict(x="Time", y="Edge ID", color="Occupancy (%)"),
                                            title="Edge Occupancy Heatmap",
                                            color_continuous_scale='Reds')
                    st.plotly_chart(fig_edge_occ, use_container_width=True)
            
            # Emissions over time
            if 'emissions_data' in st.session_state and st.session_state.emissions_data:
                st.markdown("---")
                st.markdown("#### 🌍 Emissions Timeline")
                
                df_emissions = pd.DataFrame(st.session_state.emissions_data)
                
                if 'time' in df_emissions.columns:
                    # Group by time and sum emissions
                    emissions_timeline = df_emissions.groupby('time').sum().reset_index()
                    
                    fig_emissions_time = go.Figure()
                    fig_emissions_time.add_trace(go.Scatter(x=emissions_timeline['time'], y=emissions_timeline['CO2'],
                                                            mode='lines', name='CO2', fill='tozeroy',
                                                            line=dict(color='#ef4444')))
                    fig_emissions_time.add_trace(go.Scatter(x=emissions_timeline['time'], y=emissions_timeline['NOx'],
                                                            mode='lines', name='NOx', fill='tozeroy',
                                                            line=dict(color='#8b5cf6')))
                    
                    fig_emissions_time.update_layout(
                        title="Cumulative Emissions Over Time",
                        xaxis_title="Time (s)",
                        yaxis_title="Emissions (mg)",
                        height=400
                    )
                    st.plotly_chart(fig_emissions_time, use_container_width=True)
    
    # --- EXPORT TAB ---
    with tab4:
        st.markdown("### 📋 Export Analysis Report")
        
        if 'trips_data' not in st.session_state or not st.session_state.trips_data:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.03); padding: 2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); text-align: center; margin: 2rem 0; backdrop-filter: blur(5px);'>
                <h3 style='color: #a78bfa; margin-bottom: 1rem;'>📤 No Data Available</h3>
                <p style='color: #e2e8f0; font-size: 1.1rem;'>Please upload a <strong>tripinfo.xml</strong> file first in <strong>"Upload & Parse"</strong> tab above.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            df = pd.DataFrame(st.session_state.trips_data)
            
            st.markdown('<p style="color: #cbd5e1; font-size: 1.05rem; margin-bottom: 1.5rem; font-weight: 500;">Export your simulation data in various formats for further analysis, reporting, or integration with other tools.</p>', unsafe_allow_html=True)
            
            st.markdown("#### 📊 Statistical Summary")
            
            stats_summary = df[['duration', 'waitingTime', 'timeLoss']].describe()
            st.dataframe(stats_summary, use_container_width=True)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📄 Export as CSV")
                st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">Comma-separated values for spreadsheet applications</p>', unsafe_allow_html=True)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name="sumo_analysis.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="export_csv"
                )
            
            with col2:
                st.markdown("#### 📊 Export as Excel")
                st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">Multi-sheet Excel workbook with data and statistics</p>', unsafe_allow_html=True)
                try:
                    from io import BytesIO
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Trips', index=False)
                        stats_summary.to_excel(writer, sheet_name='Statistics')
                    buffer.seek(0)
                    
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=buffer,
                        file_name="sumo_analysis.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key="export_excel"
                    )
                except ImportError:
                    st.warning("⚠️ Install openpyxl for Excel export: `pip install openpyxl`")
                except Exception as e:
                    st.error(f"❌ Excel export error: {str(e)}")
            
            st.markdown("---")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("#### 📝 Export as JSON")
                st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">JSON format for web applications and APIs</p>', unsafe_allow_html=True)
                import json
                json_data = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json_data,
                    file_name="sumo_analysis.json",
                    mime="application/json",
                    use_container_width=True,
                    key="export_json"
                )
            
            with col4:
                st.markdown("#### 📐 Export LaTeX Table")
                st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">LaTeX format for academic papers and reports</p>', unsafe_allow_html=True)
                latex_table = stats_summary.to_latex(float_format="%.2f")
                st.download_button(
                    label="⬇️ Download LaTeX",
                    data=latex_table,
                    file_name="sumo_table.tex",
                    mime="text/plain",
                    use_container_width=True,
                    key="export_latex"
                )
            
            st.markdown("---")
            st.markdown("#### 📊 Generate Comprehensive Report")
            
            col_pdf1, col_pdf2 = st.columns([2, 1])
            
            with col_pdf1:
                st.markdown('<p style="color: #cbd5e1; font-weight: 500;">Generate a complete analysis report with all visualizations and statistics.</p>', unsafe_allow_html=True)
            
            with col_pdf2:
                if st.button("📝 Generate PDF Report", type="primary", use_container_width=True):
                    st.markdown("""
                    <div style='background: rgba(255,255,255,0.03); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-top: 1rem; backdrop-filter: blur(5px);'>
                        <p style='color: #a78bfa; font-weight: 600; margin: 0;'>📋 PDF generation coming soon!</p>
                        <p style='color: #94a3b8; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>For now, export CSV/Excel and create report manually using your preferred tool.</p>
                    </div>
                    """, unsafe_allow_html=True)


# =============================================================================
# SIGNAL DESIGNER
# =============================================================================

def show_signal_designer():
    st.markdown('<h1>🚦 Signal Designer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-weight: 500;">Design and optimize traffic signals</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Phase Editor", "⏱️ Webster's Optimization", "🔄 Coordination", "📊 Capacity Analysis"])
    
    # --- PHASE EDITOR TAB ---
    with tab1:
        st.markdown("### 🎨 Visual Traffic Signal Phase Editor")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Signal Configuration")
            
            junction_id = st.text_input("Junction ID", "C", help="ID of the junction with traffic lights")
            signal_type = st.selectbox("Signal Type", ["static", "actuated", "delay_based"], 
                                      help="Type of traffic light controller")
            
            num_phases = st.number_input("Number of Phases", min_value=2, max_value=8, value=4, 
                                        help="Total number of signal phases")
            
            st.markdown("---")
            st.markdown("#### Define Phases")
            
            if 'signal_phases' not in st.session_state:
                st.session_state.signal_phases = []
            
            for i in range(num_phases):
                with st.expander(f"Phase {i+1}", expanded=(i < 2)):
                    phase_duration = st.number_input(f"Duration (s)", min_value=5, max_value=120, value=30, key=f"dur_{i}")
                    
                    state_help = "Enter signal state (G=Green, y=yellow, r=red). Example: 'GGGrrr' for 3 green, 3 red"
                    phase_state = st.text_input(f"State", "GGGrrr", key=f"state_{i}", help=state_help)
                    
                    min_dur = st.number_input(f"Min Duration (actuated)", min_value=5, max_value=60, value=10, key=f"min_{i}")
                    max_dur = st.number_input(f"Max Duration (actuated)", min_value=10, max_value=120, value=60, key=f"max_{i}")
                    
                    if st.button(f"Save Phase {i+1}", key=f"save_{i}"):
                        phase_data = {
                            "duration": phase_duration,
                            "state": phase_state,
                            "minDur": min_dur,
                            "maxDur": max_dur
                        }
                        if len(st.session_state.signal_phases) <= i:
                            st.session_state.signal_phases.append(phase_data)
                        else:
                            st.session_state.signal_phases[i] = phase_data
                        st.success(f"✅ Phase {i+1} saved!")
        
        with col2:
            st.markdown("#### Preview & Generate")
            
            if st.session_state.signal_phases:
                st.markdown("**Current Phases:**")
                total_cycle = 0
                for i, phase in enumerate(st.session_state.signal_phases):
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 8px;">
                        <strong>Phase {i+1}</strong><br>
                        Duration: {phase['duration']}s<br>
                        State: <code style="background: #2d3748; padding: 2px 4px; border-radius: 4px; color: #f8fafc;">{phase['state']}</code>
                    </div>
                    """, unsafe_allow_html=True)
                    total_cycle += phase['duration']
                
                st.metric("Total Cycle Length", f"{total_cycle} seconds")
                
                st.markdown("---")
                
                if st.button("🔨 Generate Traffic Light File", type="primary", use_container_width=True):
                    try:
                        import xml.etree.ElementTree as ET
                        
                        tl = TrafficLight(id=junction_id, type=signal_type, programID="0")
                        for phase_data in st.session_state.signal_phases:
                            tl.add_phase(Phase(
                                duration=phase_data['duration'],
                                state=phase_data['state'],
                                min_dur=phase_data['minDur'],
                                max_dur=phase_data['maxDur']
                            ))
                        
                        os.makedirs("outputs", exist_ok=True)
                        output_path = "outputs/custom_signals.tll.xml"
                        
                        root = ET.Element("additional")
                        tl_elem = tl.to_xml()
                        root.append(tl_elem)
                        
                        tree = ET.ElementTree(root)
                        ET.indent(tree, space="    ")
                        tree.write(output_path, encoding="utf-8", xml_declaration=True)
                        
                        st.success("✅ Traffic light file generated!")
                        
                        with open(output_path, 'r') as f:
                            tl_content = f.read()
                        
                        st.download_button(
                            label="⬇️ Download custom_signals.tll.xml",
                            data=tl_content,
                            file_name="custom_signals.tll.xml",
                            mime="application/xml",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.info("Define and save phases to see preview")
    
    # --- WEBSTER'S OPTIMIZATION TAB ---
    with tab2:
        st.markdown("### ⏱️ Webster's Method for Optimal Signal Timing")
        st.markdown("Minimize delay using the Webster formula for optimal cycle length")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Input Parameters")
            
            lost_time = st.number_input("Lost Time per Phase (s)", min_value=1, max_value=10, value=3,
                                       help="Time lost during each phase change (startup + clearance)")
            
            num_approaches = st.number_input("Number of Approaches", min_value=2, max_value=8, value=4)
            
            flows = []
            saturations = []
            
            for i in range(num_approaches):
                with st.expander(f"Approach {i+1}"):
                    flow = st.number_input(f"Traffic Flow (veh/h)", min_value=0, max_value=3000, value=800, key=f"flow_{i}")
                    saturation = st.number_input(f"Saturation Flow (veh/h)", min_value=1000, max_value=3600, 
                                                value=1800, key=f"sat_{i}",
                                                help="Maximum flow capacity when green")
                    flows.append(flow)
                    saturations.append(saturation)
        
        with col2:
            st.markdown("#### Optimization Results")
            
            if st.button("🧮 Calculate Optimal Timing", type="primary"):
                try:
                    # Calculate critical flow ratios (y_i = q_i / s_i)
                    flow_ratios = [q/s for q, s in zip(flows, saturations)]
                    Y = sum(flow_ratios)  # Sum of critical flow ratios
                    
                    # Webster's formula for optimal cycle length
                    L = lost_time * num_approaches  # Total lost time
                    C_opt = (1.5 * L + 5) / (1 - Y)
                    
                    # Ensure reasonable bounds
                    C_opt = max(30, min(C_opt, 180))
                    
                    # Calculate green times proportionally
                    effective_green_time = C_opt - L
                    green_times = []
                    
                    for ratio in flow_ratios:
                        g_i = (ratio / Y) * effective_green_time
                        green_times.append(g_i)
                    
                    st.success("✅ Optimization Complete!")
                    
                    st.markdown("**Optimal Cycle Length:**")
                    st.metric("Cycle Time", f"{C_opt:.1f} seconds")
                    
                    st.markdown("---")
                    st.markdown("**Green Times per Approach:**")
                    
                    for i, (g, ratio) in enumerate(zip(green_times, flow_ratios)):
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric(f"Approach {i+1}", f"{g:.1f}s")
                        col_b.metric("Flow Ratio", f"{ratio:.2f}")
                        col_c.metric("Utilization", f"{(ratio * 100):.0f}%")
                    
                    st.markdown("---")
                    st.markdown("**Performance Metrics:**")
                    avg_delay = (C_opt * (1 - Y)**2) / (2 * (1 - Y * C_opt / (C_opt - L)))
                    st.metric("Estimated Avg Delay", f"{avg_delay:.1f} seconds")
                    
                    # Save optimal timing
                    if st.button("💾 Save as Traffic Light Config"):
                        st.session_state.signal_phases = []
                        yellow_time = 3
                        
                        for i, g in enumerate(green_times):
                            # Green phase
                            state_green = "G" * num_approaches
                            st.session_state.signal_phases.append({
                                "duration": int(g),
                                "state": state_green[i] + "r" * (num_approaches - 1),
                                "minDur": int(g * 0.5),
                                "maxDur": int(g * 1.5)
                            })
                            # Yellow phase
                            state_yellow = state_green[i] + "r" * (num_approaches - 1)
                            state_yellow = state_yellow.replace("G", "y")
                            st.session_state.signal_phases.append({
                                "duration": yellow_time,
                                "state": state_yellow,
                                "minDur": yellow_time,
                                "maxDur": yellow_time
                            })
                        
                        st.success("✅ Saved! Go to Phase Editor tab to generate file.")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Ensure Y < 1.0 (total flow ratio must be less than 1)")
    
    # --- COORDINATION TAB ---
    with tab3:
        st.markdown("### 🔄 Signal Coordination & Green Wave")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Corridor Configuration")
            
            num_signals = st.number_input("Number of Signals", min_value=2, max_value=10, value=3)
            common_cycle = st.number_input("Common Cycle Length (s)", min_value=30, max_value=180, value=90)
            speed_limit = st.number_input("Speed Limit (km/h)", min_value=20, max_value=120, value=50)
            
            distances = []
            for i in range(num_signals - 1):
                dist = st.number_input(f"Distance Signal {i+1} to {i+2} (m)", 
                                      min_value=50, max_value=1000, value=300, key=f"dist_{i}")
                distances.append(dist)
        
        with col2:
            st.markdown("#### Calculate Offsets")
            
            if st.button("🧮 Calculate Green Wave Offsets", type="primary"):
                try:
                    speed_ms = speed_limit / 3.6  # Convert to m/s
                    
                    st.success("✅ Offsets Calculated!")
                    
                    offsets = [0]  # First signal has 0 offset
                    for dist in distances:
                        travel_time = dist / speed_ms
                        offset = offsets[-1] + travel_time
                        offset = offset % common_cycle  # Wrap around cycle
                        offsets.append(offset)
                    
                    st.markdown("**Signal Offsets:**")
                    for i, offset in enumerate(offsets):
                        st.metric(f"Signal {i+1}", f"{offset:.1f} seconds")
                    
                    st.markdown("---")
                    st.markdown("**Configuration Summary:**")
                    st.markdown(f"<p style='color: #cbd5e1;'>- Common cycle: {common_cycle}s</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #cbd5e1;'>- Progression speed: {speed_limit} km/h</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #cbd5e1;'>- Total corridor length: {sum(distances):.0f}m</p>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # --- CAPACITY ANALYSIS TAB ---
    with tab4:
        st.markdown("### 📊 Intersection Capacity Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Input Data")
            
            analysis_type = st.selectbox("Analysis Type", 
                                        ["Signalized Intersection", "Unsignalized Intersection", "Roundabout"])
            
            if analysis_type == "Signalized Intersection":
                num_lanes_ns = st.number_input("Lanes (North-South)", min_value=1, max_value=4, value=2)
                num_lanes_ew = st.number_input("Lanes (East-West)", min_value=1, max_value=4, value=2)
                cycle_length = st.number_input("Cycle Length (s)", min_value=30, max_value=180, value=90)
                green_time_ns = st.number_input("Green Time NS (s)", min_value=10, max_value=120, value=40)
                green_time_ew = st.number_input("Green Time EW (s)", min_value=10, max_value=120, value=40)
                saturation_flow_per_lane = st.number_input("Saturation Flow (veh/h/lane)", 
                                                           min_value=1000, max_value=2200, value=1800)
        
        with col2:
            st.markdown("#### Analysis Results")
            
            if st.button("📊 Analyze Capacity", type="primary"):
                try:
                    if analysis_type == "Signalized Intersection":
                        # Calculate capacity
                        capacity_ns = num_lanes_ns * saturation_flow_per_lane * (green_time_ns / cycle_length)
                        capacity_ew = num_lanes_ew * saturation_flow_per_lane * (green_time_ew / cycle_length)
                        
                        total_capacity = capacity_ns + capacity_ew
                        
                        st.success("✅ Analysis Complete!")
                        
                        col_a, col_b = st.columns(2)
                        col_a.metric("NS Capacity", f"{capacity_ns:.0f} veh/h")
                        col_b.metric("EW Capacity", f"{capacity_ew:.0f} veh/h")
                        
                        st.metric("Total Capacity", f"{total_capacity:.0f} veh/h")
                        
                        # Level of Service estimation
                        st.markdown("---")
                        st.markdown("**Level of Service Thresholds:**")
                        st.markdown(f"<p style='color: #cbd5e1;'>- LOS A: < {total_capacity * 0.6:.0f} veh/h (Free flow)</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #cbd5e1;'>- LOS B: {total_capacity * 0.6:.0f} - {total_capacity * 0.7:.0f} veh/h</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #cbd5e1;'>- LOS C: {total_capacity * 0.7:.0f} - {total_capacity * 0.8:.0f} veh/h</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #cbd5e1;'>- LOS D: {total_capacity * 0.8:.0f} - {total_capacity * 0.9:.0f} veh/h</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #cbd5e1;'>- LOS E: {total_capacity * 0.9:.0f} - {total_capacity:.0f} veh/h (At capacity)</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #cbd5e1;'>- LOS F: > {total_capacity:.0f} veh/h (Oversaturated)</p>", unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


# =============================================================================
# DOCUMENTATION BROWSER
# =============================================================================

def show_documentation_browser():
    st.markdown('<h1>📚 SUMO Documentation</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-weight: 500;">Browse and search official SUMO documentation</p>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Initialize documentation browser
    try:
        from src.rag.vector_store import SUMOVectorStore
        from src.docs_browser import DocumentationBrowser

        # Load vector store
        with st.spinner("Loading documentation database..."):
            vector_store = SUMOVectorStore(persist_directory="vector_db")

        browser = DocumentationBrowser(vector_store)

        # Get statistics
        stats = vector_store.get_stats()

        # Show status
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 Total Documents", stats['total_documents'])
        with col2:
            categories = browser.get_categories()
            st.metric("📂 Categories", len(categories))
        with col3:
            st.metric("🔖 Bookmarks", len(st.session_state.doc_bookmarks))
        with col4:
            st.metric("💾 Database Size", f"{stats['index_size_mb']:.1f} MB")

        st.markdown("---")

        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📂 Browse by Category", "🔖 Bookmarks", "ℹ️ About"])

        # ===== SEARCH TAB =====
        with tab1:
            st.markdown("### 🔍 Search Documentation")
            st.markdown("Use semantic search to find relevant SUMO documentation")

            search_query = st.text_input(
                "Search query:",
                placeholder="e.g., 'How to create traffic lights', 'Car following models', 'Route definition'...",
                key="doc_search"
            )

            col1, col2 = st.columns([3, 1])
            with col1:
                num_results = st.slider("Number of results", 5, 20, 10, key="search_results")
            with col2:
                search_button = st.button("🔍 Search", type="primary", use_container_width=True)

            if search_query and (search_button or search_query):
                with st.spinner("Searching..."):
                    results = browser.search_documents(search_query, n_results=num_results)

                if results:
                    st.success(f"Found {len(results)} relevant documents")

                    for i, doc in enumerate(results, 1):
                        with st.expander(f"**{i}. {doc['title']}** ({doc['category']}) - Relevance: {doc['similarity']:.2%}"):
                            col1, col2 = st.columns([4, 1])

                            with col1:
                                st.markdown(f"**Category:** {doc['category']}")
                                st.markdown(f"**Preview:**\n{doc['preview']}")
                                st.markdown(f"[📖 View full documentation]({doc['url']})")

                            with col2:
                                if browser.is_bookmarked(doc['title']):
                                    if st.button("❤️ Saved", key=f"unbookmark_{i}", use_container_width=True):
                                        browser.remove_bookmark(doc['title'])
                                        st.rerun()
                                else:
                                    if st.button("🤍 Save", key=f"bookmark_{i}", use_container_width=True):
                                        browser.add_bookmark(doc['title'], doc['category'], doc['url'])
                                        st.success("Bookmarked!")
                                        st.rerun()

                            # Show related documents
                            if st.checkbox(f"Show related docs", key=f"related_{i}"):
                                related = browser.find_related_documents(doc['title'], n_results=3)
                                if related:
                                    st.markdown("**Related documents:**")
                                    for j, rel in enumerate(related, 1):
                                        st.markdown(f"{j}. [{rel['title']}]({rel['url']}) ({rel['category']})")
                else:
                    st.info("No documents found. Try a different search query.")

        # ===== BROWSE BY CATEGORY TAB =====
        with tab2:
            st.markdown("### 📂 Browse by Category")
            st.markdown("Explore documentation organized by topic")

            categories = browser.get_categories()

            if categories:
                # Category selector
                selected_category = st.selectbox(
                    "Select a category:",
                    options=list(categories.keys()),
                    format_func=lambda x: f"{x} ({categories[x]} documents)",
                    key="category_select"
                )

                if selected_category:
                    st.markdown(f"#### 📑 {selected_category}")
                    st.markdown(f"*{categories[selected_category]} documents in this category*")
                    st.markdown("---")

                    # Get documents in category
                    docs = browser.get_documents_by_category(selected_category)

                    # Display documents
                    for i, doc in enumerate(docs, 1):
                        with st.expander(f"**{i}. {doc['title']}**"):
                            col1, col2 = st.columns([4, 1])

                            with col1:
                                st.markdown(f"**Preview:**\n{doc['preview']}")
                                st.markdown(f"[📖 View full documentation]({doc['url']})")

                            with col2:
                                if browser.is_bookmarked(doc['title']):
                                    if st.button("❤️ Saved", key=f"cat_unbookmark_{i}", use_container_width=True):
                                        browser.remove_bookmark(doc['title'])
                                        st.rerun()
                                else:
                                    if st.button("🤍 Save", key=f"cat_bookmark_{i}", use_container_width=True):
                                        browser.add_bookmark(doc['title'], doc['category'], doc['url'])
                                        st.success("Bookmarked!")
                                        st.rerun()

            else:
                st.info("No categories available. Build the documentation database first.")

        # ===== BOOKMARKS TAB =====
        with tab3:
            st.markdown("### 🔖 Your Bookmarks")
            st.markdown("Quick access to your saved documentation")

            if st.session_state.doc_bookmarks:
                st.info(f"You have {len(st.session_state.doc_bookmarks)} bookmarked documents")

                for i, bookmark in enumerate(st.session_state.doc_bookmarks, 1):
                    with st.expander(f"**{i}. {bookmark['title']}**"):
                        col1, col2 = st.columns([4, 1])

                        with col1:
                            st.markdown(f"**Category:** {bookmark['category']}")
                            st.markdown(f"[📖 View documentation]({bookmark['url']})")

                        with col2:
                            if st.button("🗑️ Remove", key=f"remove_bookmark_{i}", use_container_width=True):
                                browser.remove_bookmark(bookmark['title'])
                                st.success("Removed from bookmarks")
                                st.rerun()

                if st.button("🗑️ Clear All Bookmarks", type="secondary"):
                    st.session_state.doc_bookmarks = []
                    browser._save_bookmarks()
                    st.success("All bookmarks cleared!")
                    st.rerun()
            else:
                st.info("📌 No bookmarks yet. Save documents while browsing to quickly access them later!")
                st.markdown("""
                **How to bookmark:**
                1. Go to 🔍 Search or 📂 Browse tabs
                2. Click 🤍 Save button on any document
                3. Access your bookmarks here anytime
                """)

        # ===== ABOUT TAB =====
        with tab4:
            st.markdown("### ℹ️ About SUMO Documentation")

            st.markdown("""
            This documentation browser provides access to the complete **SUMO (Simulation of Urban Mobility)**
            official documentation with enhanced search and navigation features.

            #### 📊 Database Information
            """)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                - **Total Documents:** {stats['total_documents']}
                - **Categories:** {len(categories)}
                - **Embedding Model:** {stats['embedding_model']}
                """)
            with col2:
                st.markdown(f"""
                - **Database Size:** {stats['index_size_mb']:.2f} MB
                - **Vector Dimensions:** {stats['embedding_dim']}
                - **Search Type:** Semantic (AI-powered)
                """)

            st.markdown("---")
            st.markdown("#### ✨ Features")
            st.markdown("""
            - **🔍 Semantic Search:** Find documents by meaning, not just keywords
            - **📂 Category Browsing:** Organized by topic for easy navigation
            - **🔖 Bookmarks:** Save frequently accessed documents
            - **🔗 Related Docs:** Discover connected documentation
            - **⚡ Fast:** Sub-second search across 497 documents
            """)

            st.markdown("---")
            st.markdown("#### 🔧 Maintenance")

            if st.button("🔄 Rebuild Documentation Database"):
                st.warning("This will rebuild the entire documentation database. It may take 1-2 minutes.")
                if st.button("✅ Confirm Rebuild"):
                    with st.spinner("Rebuilding database..."):
                        try:
                            from src.rag.doc_parser import SUMODocParser
                            parser = SUMODocParser()
                            docs = parser.parse_all_docs()
                            vector_store.clear_collection()
                            vector_store.add_documents(docs)
                            st.success(f"✅ Database rebuilt! {len(docs)} documents indexed.")
                        except Exception as e:
                            st.error(f"❌ Error rebuilding database: {e}")

    except FileNotFoundError:
        st.error("❌ Documentation database not found!")
        st.markdown("""
        The vector database needs to be built first. Please run:

        ```bash
        python build_vector_db.py
        ```

        This will index all 497 SUMO documentation files (takes ~1-2 minutes).
        """)

    except Exception as e:
        st.error(f"❌ Error loading documentation browser: {e}")
        st.markdown("Please ensure the RAG system is properly set up.")


# =============================================================================
# AI ASSISTANT
# =============================================================================

def show_ai_assistant():
    st.markdown('<h1>🤖 AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-weight: 500;">Get intelligent help with your simulation</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "🎯 Scenario Generator", "🔧 Troubleshooter"])
    
    # --- CHAT ASSISTANT TAB ---
    with tab1:
        st.markdown("### 💬 Ask the AI Assistant")
        
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = None
        
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:  # Catch all exceptions including StreamlitSecretNotFoundError
            pass
        
        if not api_key:
            api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key:
            st.warning("⚠️ Groq API key not configured")
            st.markdown("""
            **To enable AI Assistant:**
            
            **For Local Development:**
            1. Get a free API key from [Groq Console](https://console.groq.com)
            2. Open the `.env` file in the project root
            3. Replace `your_api_key_here` with your actual key
            4. Restart the application
            
            **For Streamlit Cloud:**
            1. Go to your app dashboard on share.streamlit.io
            2. Click "⚙️ Settings" → "Secrets"
            3. Add: `GROQ_API_KEY = "your_key_here"`
            4. Save and the app will restart automatically
            """)
            
            api_key = st.text_input("Or enter API key temporarily (not saved):", type="password")
        
        if api_key:
            try:
                from groq import Groq
                
                st.markdown("#### 🤖 Select AI Model")
                model_choice = st.selectbox(
                    "Choose model for chat:",
                    [
                        "llama-3.3-70b-versatile (Balanced, recommended)",
                        "llama-3.1-70b-versatile (Alternative 70B)",
                        "llama-3.3-70b-specdec (Speculative decoding)",
                        "mixtral-8x7b-32768 (Good context window)",
                        "gemma2-9b-it (Fast & efficient)"
                    ],
                    key="chat_model"
                )
                
                model_map = {
                    "llama-3.3-70b-versatile (Balanced, recommended)": "llama-3.3-70b-versatile",
                    "llama-3.1-70b-versatile (Alternative 70B)": "llama-3.1-70b-versatile",
                    "llama-3.3-70b-specdec (Speculative decoding)": "llama-3.3-70b-specdec",
                    "mixtral-8x7b-32768 (Good context window)": "mixtral-8x7b-32768",
                    "gemma2-9b-it (Fast & efficient)": "gemma2-9b-it"
                }
                selected_model = model_map[model_choice]

                # RAG Toggle
                use_rag = st.checkbox(
                    "📚 Use Official SUMO Documentation (RAG-Enhanced Answers)",
                    value=True,
                    help="When enabled, AI will reference official SUMO documentation to provide verified, citation-backed answers"
                )

                # Initialize RAG engine if enabled
                rag_engine = None
                rag_status_msg = ""
                if use_rag:
                    try:
                        from src.rag.rag_engine import SUMORagEngine
                        rag_engine = SUMORagEngine(api_key)
                        status = rag_engine.get_status()
                        if status['ready']:
                            rag_status_msg = f"✅ Documentation database loaded ({status['total_documents']} documents indexed)"
                        else:
                            rag_status_msg = "⚠️ Documentation database not built yet. Run `python build_vector_db.py` first. Using standard mode."
                            rag_engine = None
                    except Exception as e:
                        rag_status_msg = f"⚠️ Could not load documentation: {str(e)[:100]}... Using standard mode."
                        rag_engine = None

                    if rag_status_msg:
                        st.info(rag_status_msg)

                st.markdown("---")

                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                
                user_input = st.chat_input("Ask about SUMO simulation, network design, or traffic analysis...")
                
                if user_input:
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    
                    with st.chat_message("user"):
                        st.markdown(user_input)
                    
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            try:
                                # Use RAG if enabled and available
                                if rag_engine:
                                    result = rag_engine.query(user_input, n_results=3, model=selected_model)
                                    ai_response = result['answer']
                                    st.markdown(ai_response)

                                    # Display sources
                                    if result.get('sources'):
                                        with st.expander("📚 Sources from SUMO Documentation", expanded=False):
                                            for i, source in enumerate(result['sources'], 1):
                                                st.markdown(f"**{i}. {source['title']}**")
                                                st.markdown(f"*Category: {source['category']}*")
                                                st.markdown(f"```\n{source['preview'][:300]}...\n```")
                                                st.markdown(f"[View in docs]({source['url']})")
                                                if i < len(result['sources']):
                                                    st.markdown("---")
                                else:
                                    # Standard mode without RAG
                                    client = Groq(api_key=api_key)

                                    system_prompt = """You are an expert in traffic simulation using SUMO (Simulation of Urban Mobility).
                                    You help users design networks, configure traffic flows, optimize signals, and analyze simulation results.
                                    Provide clear, practical advice with specific parameter values when possible.
                                    If asked about SUMO XML formats, provide examples.
                                    Be concise but informative."""

                                    messages = [{"role": "system", "content": system_prompt}]
                                    messages.extend([{"role": m["role"], "content": m["content"]}
                                                   for m in st.session_state.chat_history])

                                    response = client.chat.completions.create(
                                        model=selected_model,
                                        messages=messages,
                                        temperature=0.7,
                                        max_tokens=1024,
                                    )

                                    ai_response = response.choices[0].message.content
                                    st.markdown(ai_response)

                                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("🗑️ Clear Chat History"):
                        st.session_state.chat_history = []
                        st.rerun()
            
            except ImportError:
                st.error("❌ Groq library not installed. Run: `pip install groq`")
        else:
            st.info("💡 Enter an API key to start chatting with the AI assistant")
    
    # --- SCENARIO GENERATOR TAB ---
    with tab2:
        st.markdown("### 🎯 AI-Powered Scenario Generator")
        st.markdown("Describe your simulation scenario in natural language, and AI will help generate it.")
        
        scenario_model = st.selectbox(
            "Select model for scenario generation:",
            [
                "llama-3.3-70b-versatile (Best for scenarios)",
                "llama-3.1-70b-versatile (Alternative)",
                "mixtral-8x7b-32768 (Large context)",
                "gemma2-9b-it (Fast generation)"
            ],
            key="scenario_model"
        )
        
        scenario_model_map = {
            "llama-3.3-70b-versatile (Best for scenarios)": "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile (Alternative)": "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768 (Large context)": "mixtral-8x7b-32768",
            "gemma2-9b-it (Fast generation)": "gemma2-9b-it"
        }
        selected_scenario_model = scenario_model_map[scenario_model]
        
        scenario_description = st.text_area(
            "Describe your scenario:",
            placeholder="Example: I need a 4-way intersection with heavy north-south traffic during rush hour, moderate east-west traffic, and a traffic light optimized for minimal delay.",
            height=150
        )
        
        if st.button("🤖 Generate Scenario Recommendations", type="primary"):
            if not api_key:
                st.warning("⚠️ Please configure Groq API key first")
            elif scenario_description:
                try:
                    from groq import Groq
                    client = Groq(api_key=api_key)
                    
                    prompt = f"""Based on this traffic simulation scenario description:
                    
"{scenario_description}"

Please provide specific recommendations for ClickSUMO configuration in this format:

1. **Network Template**: [Which template to use and why]
2. **Network Parameters**:
   - Arm length: [value in meters]
   - Number of lanes: [value]
   - Speed limit: [value in km/h]
3. **Traffic Demand**:
   - North-South flow: [vehicles/hour]
   - East-West flow: [vehicles/hour]
   - Vehicle types: [types to use]
4. **Signal Timing**:
   - Cycle length: [seconds]
   - Phase splits: [how to divide green time]
5. **Expected Outcomes**: [What to expect from this configuration]

Be specific with numbers."""
                    
                    with st.spinner("Analyzing scenario..."):
                        response = client.chat.completions.create(
                            model=selected_scenario_model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.5,
                            max_tokens=1500,
                        )
                        
                        recommendations = response.choices[0].message.content
                        st.markdown("### 📋 AI Recommendations")
                        st.markdown(recommendations)
                        
                        st.success("✅ Recommendations generated! Use these parameters in Network Studio and Demand Generator.")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please describe your scenario first")
    
    # --- TROUBLESHOOTER TAB ---
    with tab3:
        st.markdown("### 🔧 Intelligent Troubleshooter")
        
        st.markdown("Having issues with your simulation? Describe problem and get AI-powered solutions.")
        
        troubleshoot_model = st.selectbox(
            "Select model for troubleshooting:",
            [
                "llama-3.3-70b-versatile (Best for diagnosis)",
                "llama-3.1-70b-versatile (Alternative)",
                "mixtral-8x7b-32768 (Detailed analysis)",
                "gemma2-9b-it (Quick fixes)"
            ],
            key="troubleshoot_model"
        )
        
        troubleshoot_model_map = {
            "llama-3.3-70b-versatile (Best for diagnosis)": "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile (Alternative)": "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768 (Detailed analysis)": "mixtral-8x7b-32768",
            "gemma2-9b-it (Quick fixes)": "gemma2-9b-it"
        }
        selected_troubleshoot_model = troubleshoot_model_map[troubleshoot_model]
        
        issue_type = st.selectbox(
            "Issue Category:",
            ["Simulation won't run", "Network errors", "Traffic flow issues", 
             "Signal timing problems", "Performance issues", "Other"]
        )
        
        issue_description = st.text_area(
            "Describe the issue:",
            placeholder="Example: My vehicles are getting stuck at the intersection and not moving through the green light.",
            height=150
        )
        
        error_log = st.text_area(
            "Error messages or log (optional):",
            placeholder="Paste any error messages here...",
            height=100
        )
        
        if st.button("🔍 Diagnose Problem", type="primary"):
            if not api_key:
                st.warning("⚠️ Please configure Groq API key first")
            elif issue_description:
                try:
                    from groq import Groq
                    client = Groq(api_key=api_key)
                    
                    prompt = f"""I'm having a SUMO traffic simulation issue:

**Category**: {issue_type}
**Problem**: {issue_description}
"""
                    
                    if error_log:
                        prompt += f"\n**Error Log**:\n{error_log}\n"
                    
                    prompt += """
Please provide:
1. **Diagnosis**: What is likely causing this issue?
2. **Solution**: Step-by-step instructions to fix it
3. **Prevention**: How to avoid this in the future
4. **Related Tips**: Any additional advice

Be specific and practical."""
                    
                    with st.spinner("Analyzing issue..."):
                        response = client.chat.completions.create(
                            model=selected_troubleshoot_model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.3,
                            max_tokens=1500,
                        )
                        
                        diagnosis = response.choices[0].message.content
                        st.markdown("### 🔧 Diagnosis & Solution")
                        st.markdown(diagnosis)
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please describe the issue first")
        
        with st.expander("💡 Common Issues & Quick Fixes"):
            st.markdown("""
            **Vehicles stuck at intersection:**
            - Check connection definitions in network
            - Verify traffic light state strings match number of connections
            - Ensure edges are properly connected
            
            **High waiting times:**
            - Optimize signal timing (use Webster's method)
            - Check if traffic demand exceeds capacity
            - Consider adding more lanes
            
            **Simulation crashes:**
            - Validate all XML files with SUMO's netconvert
            - Check for negative values or missing required attributes
            - Ensure route edges form valid paths
            
            **No vehicles appearing:**
            - Check route file has flows/vehicles defined
            - Verify begin/end times match simulation duration
            - Confirm edge IDs in routes match network edges
            """)


# =============================================================================
# MAIN ROUTING
# =============================================================================

if "🏠 Home" in page:
    show_home()
elif "🛣️ Network Studio" in page:
    show_network_studio()
elif "🚗 Demand Generator" in page:
    show_demand_generator()
elif "🚦 Signal Designer" in page:
    show_signal_designer()
elif "📊 Output Analyzer" in page:
    show_output_analyzer()
elif "📚 Documentation" in page:
    show_documentation_browser()
elif "🤖 AI Assistant" in page:
    show_ai_assistant()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 1rem; margin-top: 3rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; backdrop-filter: blur(10px);'>
    <h2 style='background: linear-gradient(to right, #8b5cf6, #d946ef); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>ClickSUMO</h2>
    <p style='color: #a78bfa; font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0; letter-spacing: 0.05em;'>Created by Mahbub Hassan</p>
    <p style='color: #cbd5e1; font-size: 0.95rem; margin: 0.8rem 0 0; font-weight: 500;'>Making Traffic Simulation Accessible to Everyone</p>
    <p style='color: #64748b; font-size: 0.8rem; margin-top: 1.5rem;'>version8.0 (NEBULA AI) | © 2026</p>
</div>
""", unsafe_allow_html=True)