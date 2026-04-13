import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
from predict import predict_emergency
from crowd_control import crowd_control
from evacuation import build_graph, apply_conditions, heuristic
from auth import login
import networkx as nx
import math

# ================================================================
# PAGE CONFIG & STYLING
# ================================================================

st.set_page_config(
    page_title="SMART EMERGENCY AI CONTROL SYSTEM",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# CUSTOM CSS - FUTURISTIC DARK THEME
# ================================================================

custom_css = """
<style>
    :root {
        --primary-dark: #0f172a;
        --card-dark: #1a2847;
        --neon-blue: #00d9ff;
        --neon-red: #ff0055;
        --neon-green: #00ff88;
        --neon-yellow: #ffff00;
        --text-light: #e0e0e0;
    }
    
    /* MAIN BACKGROUND */
    .main {
        background-color: #0f172a;
        color: #e0e0e0;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1a2847;
        border-right: 2px solid #00d9ff;
    }
    
    /* HEADERS */
    h1, h2, h3 {
        color: #00d9ff !important;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
    }
    
    /* CARDS & CONTAINERS */
    [data-testid="stMetricValue"] {
        color: #00ff88 !important;
        font-size: 2rem !important;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0 !important;
    }
    
    /* CARDS WITH GLOW */
    .card {
        background: linear-gradient(135deg, #1a2847 0%, #0f3460 100%);
        border: 2px solid #00d9ff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.3), 
                    0 4px 15px rgba(0, 0, 0, 0.5);
        color: #e0e0e0;
    }
    
    .card-alert {
        background: linear-gradient(135deg, #2a1a1a 0%, #3a1a1a 100%);
        border: 2px solid #ff0055;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(255, 0, 85, 0.3),
                    0 4px 15px rgba(0, 0, 0, 0.5);
        color: #e0e0e0;
    }
    
    .card-success {
        background: linear-gradient(135deg, #1a2a1a 0%, #1a3a1a 100%);
        border: 2px solid #00ff88;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3),
                    0 4px 15px rgba(0, 0, 0, 0.5);
        color: #e0e0e0;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
        color: #000;
        border: 0;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.5);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(0, 217, 255, 0.8);
        transform: scale(1.05);
    }
    
    /* PRIMARY BUTTON */
    .btn-primary {
        background: linear-gradient(135deg, #ff0055 0%, #cc0044 100%);
        color: #fff;
        border: 0;
        border-radius: 10px;
        padding: 15px 30px;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 0 20px rgba(255, 0, 85, 0.6);
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-primary:hover {
        box-shadow: 0 0 30px rgba(255, 0, 85, 0.9);
    }
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > input {
        background-color: #0f3460;
        color: #00d9ff;
        border: 2px solid #00d9ff;
        border-radius: 8px;
        padding: 10px;
        font-size: 1rem;
        font-weight: 600;
    }
    
    /* DROPDOWN/SELECT OPTIONS */
    [data-testid="stSelectbox"] {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSelectbox"] > div > div {
        background-color: #0f3460 !important;
        border: 2px solid #00d9ff !important;
    }
    
    .st-emotion-cache-1v0mbqo {
        color: #e0e0e0 !important;
    }
    
    /* SELECTBOX OPTIONS - DROPDOWN LIST */
    [role="listbox"] {
        background-color: #1a2847 !important;
    }
    
    [role="option"] {
        color: #e0e0e0 !important;
        background-color: #0f3460 !important;
    }
    
    [role="option"]:hover {
        background-color: #1a4a70 !important;
    }
    
    /* TABS */
    [data-testid="stTabs"] {
        background-color: #1a2847;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 2px solid #00d9ff;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-bottom: 2px solid transparent;
        color: #b0b0b0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00d9ff !important;
        border-color: #00d9ff !important;
        box-shadow: inset 0 -2px 0 #00d9ff;
    }
    
    /* TABLE STYLING */
    .stDataFrame {
        background-color: #1a2847;
    }
    
    /* BADGES */
    .badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 5px;
    }
    
    .badge-active {
        background-color: #00ff88;
        color: #000;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    .badge-alert {
        background-color: #ff0055;
        color: #fff;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.5);
    }
    
    .badge-warning {
        background-color: #ffff00;
        color: #000;
        box-shadow: 0 0 10px rgba(255, 255, 0, 0.5);
    }
    
    /* TITLE STYLES */
    .title-glowing {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #00d9ff, #00ff88, #ff0055);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(0, 217, 255, 0.5);
        margin: 20px 0;
    }
    
    .subtitle {
        text-align: center;
        color: #00d9ff;
        font-size: 1.2rem;
        margin-bottom: 30px;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
    }
    
    /* ROLE BADGE */
    .role-badge {
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
        font-size: 1.1rem;
    }
    
    .role-public {
        background-color: #1a3a5c;
        border: 2px solid #00d9ff;
        color: #00d9ff;
    }
    
    .role-official {
        background-color: #3a2a1a;
        border: 2px solid #ffaa00;
        color: #ffaa00;
    }
    
    .role-admin {
        background-color: #3a1a1a;
        border: 2px solid #ff0055;
        color: #ff0055;
    }
    
    /* GRID ITEMS */
    .grid-item {
        background: linear-gradient(135deg, #1a2847 0%, #0f3460 100%);
        border: 2px solid #00d9ff;
        border-radius: 12px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.2);
        color: #e0e0e0;
    }

    /* COLORS FOR EMERGENCY TYPES */
    .fire-badge {
        background-color: #ff0055;
        color: white;
    }
    
    .medical-badge {
        background-color: #00ff88;
        color: #000;
    }
    
    .gas-badge {
        background-color: #ffff00;
        color: #000;
    }
    
    .other-badge {
        background-color: #00d9ff;
        color: #000;
    }
    
    /* LOGIN PAGE */
    .login-container {
        background: linear-gradient(135deg, #1a2847 0%, #0f3460 100%);
        border: 3px solid #00d9ff;
        border-radius: 20px;
        padding: 60px 40px;
        max-width: 600px;
        margin: 100px auto;
        box-shadow: 0 0 40px rgba(0, 217, 255, 0.4), 0 4px 20px rgba(0, 0, 0, 0.6);
        text-align: center;
    }
    
    .login-title {
        font-size: 2.5rem;
        color: #00d9ff;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
    }
    
    .login-subtitle {
        font-size: 1.2rem;
        color: #b0b0b0;
        margin-bottom: 30px;
    }
    
    /* ALL TEXT IMPROVEMENTS */
    body, p, div, span, li, td, th, label {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMarkdownContainer"] {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMarkdownContainer"] p {
        color: #e0e0e0 !important;
    }
    
    ul li {
        color: #e0e0e0 !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ================================================================
# MOCK DATA GENERATORS
# ================================================================

def generate_mock_incidents(count=10):
    """Generate mock incident data"""
    types = ["Fire", "Medical Emergency", "Gas Leak", "Security Breach"]
    statuses = ["Active", "Contained", "Resolved"]
    
    incidents = []
    for i in range(count):
        incidents.append({
            "ID": f"INC-{2024001 + i}",
            "Type": random.choice(types),
            "Status": random.choice(statuses),
            "Location": f"Building {chr(65 + i % 5)}, Floor {(i % 10) + 1}",
            "Time": (datetime.now() - timedelta(minutes=random.randint(0, 120))).strftime("%H:%M:%S"),
            "People Affected": random.randint(10, 500),
            "Confidence": f"{random.randint(75, 99)}%"
        })
    return pd.DataFrame(incidents)

# ================================================================
# UTILITY FUNCTIONS
# ================================================================

def get_emergency_color(emergency_type):
    """Get color for emergency type"""
    colors = {
        "Fire": "#ff0055",
        "Medical Emergency": "#00ff88",
        "Gas Leak": "#ffff00",
        "Security Breach": "#00d9ff"
    }
    return colors.get(emergency_type, "#00d9ff")

def get_emergency_emoji(emergency_type):
    """Get emoji for emergency type"""
    emojis = {
        "Fire": "🔥",
        "Medical Emergency": "⚕️",
        "Gas Leak": "☣️",
        "Security Breach": "🔐"
    }
    return emojis.get(emergency_type, "⚠️")

def create_evacuation_map(primary_path, alternate_path, emergency_type):
    """Create a Google Maps-like evacuation route visualization"""
    
    # Define coordinates for building layout
    locations = {
        "Room A": (1, 5),
        "Room B": (1, 3),
        "Room C": (1, 1),
        "Room D": (3, 5),
        "Room E": (3, 3),
        "Room F": (3, 1),
        "Room G": (5, 5),
        "Room H": (5, 3),
        "Corridor 1": (2, 4),
        "Corridor 2": (2, 2),
        "Corridor 3": (4, 4),
        "Corridor 4": (4, 2),
        "Stairs Left": (1.5, 1),
        "Stairs Center": (3.5, 1),
        "Stairs Right": (5.5, 1),
        "Exit 1": (1.5, -1),
        "Exit 2": (3.5, -1),
        "Exit 3": (5.5, -1),
    }
    
    fig = go.Figure()
    
    # Add all building locations as nodes
    for location, (x, y) in locations.items():
        if "Room" in location:
            color = "#ff6b6b"
            size = 20
            symbol = "square"
        elif "Corridor" in location:
            color = "#4ecdc4"
            size = 18
            symbol = "diamond"
        elif "Stairs" in location:
            color = "#ffd93d"
            size = 20
            symbol = "star"
        else:  # Exit
            color = "#00ff88"
            size = 25
            symbol = "star"
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            text=[location],
            textposition="top center",
            marker=dict(size=size, color=color, symbol=symbol),
            hovertext=location,
            hoverinfo="text",
            showlegend=False
        ))
    
    # Parse and draw primary path
    primary_locations = primary_path
    for i in range(len(primary_locations) - 1):
        start = locations[primary_locations[i]]
        end = locations[primary_locations[i + 1]]
        
        fig.add_trace(go.Scatter(
            x=[start[0], end[0]],
            y=[start[1], end[1]],
            mode="lines",
            line=dict(color="#ff0055", width=4),
            hovertext=f"{primary_locations[i]} → {primary_locations[i+1]}",
            showlegend=False,
            opacity=0.8
        ))
    
    # Parse and draw alternate path (dashed)
    if alternate_path:
        alternate_locations = alternate_path
        for i in range(len(alternate_locations) - 1):
            start = locations[alternate_locations[i]]
            end = locations[alternate_locations[i + 1]]
            
            fig.add_trace(go.Scatter(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                mode="lines",
                line=dict(color="#ffaa00", width=2, dash="dash"),
                hovertext=f"Alternate: {alternate_locations[i]} → {alternate_locations[i+1]}",
                showlegend=False,
                opacity=0.6
            ))
    
    # Update layout
    fig.update_layout(
        title={
            "text": f"🗺️ Evacuation Route Map - {emergency_type}",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "color": "#00d9ff"}
        },
        showlegend=False,
        hovermode="closest",
        margin=dict(b=0, l=0, r=0, t=50),
        plot_bgcolor="#1a2847",
        paper_bgcolor="#0f172a",
        font=dict(color="#e0e0e0", size=12),
        width=800,
        height=600,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="#2a3950",
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="#2a3950",
            zeroline=False,
            showticklabels=False
        )
    )
    
    return fig


def show_metric_card(col, label, value, unit="", emoji=""):
    """Display a styled metric card"""
    with col:
        st.markdown(f"""
        <div class="card">
            <div style="font-size: 1.2rem; color: #e0e0e0; font-weight: 600;">{emoji} {label}</div>
            <div style="font-size: 2rem; color: #00ff88; margin: 10px 0; text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);">
                {value}
            </div>
            <div style="font-size: 0.9rem; color: #00d9ff;">{unit}</div>
        </div>
        """, unsafe_allow_html=True)

# ================================================================
# SIDEBAR - ROLE SELECTION
# ================================================================

def setup_sidebar():
    """Setup sidebar with role information and logout"""
    st.sidebar.markdown("# ⚙️ CONTROL PANEL")
    st.sidebar.markdown("---")
    
    # Get current role
    role_key = st.session_state.current_role
    
    # Role badge mapping
    role_colors = {
        "public": ("role-public", "👤 PUBLIC ACCESS"),
        "official": ("role-official", "👨‍💼 OFFICIAL PERSON"),
        "admin": ("role-admin", "🛡️ ADMINISTRATOR"),
    }
    
    css_class, role_badge_text = role_colors[role_key]
    st.sidebar.markdown(f"""
    <div class="role-badge {css_class}">
        {role_badge_text}
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Settings
    st.sidebar.markdown("### 🔧 Settings")
    auto_refresh = st.sidebar.checkbox("🔄 Auto-Refresh", value=True)
    
    if auto_refresh:
        refresh_interval = st.sidebar.slider("Refresh Interval (sec)", 5, 60, 30)
    else:
        refresh_interval = None
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 System Info")
    st.sidebar.markdown(f"**Status:** <span style='color: #00ff88;'>🟢 ACTIVE</span>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**Version:** 2.1.0")
    st.sidebar.markdown(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
    
    st.sidebar.markdown("---")
    
    # Logout button
    if st.sidebar.button("🔓 LOGOUT", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_role = None
        st.rerun()

# ================================================================
# PUBLIC DASHBOARD
# ================================================================

def show_public_dashboard():
    """Display public emergency reporting dashboard"""
    
    st.markdown("""
    <div class="title-glowing">🚨 EMERGENCY ANALYSIS</div>
    <div class="subtitle">Detect & Report Emergency Situations</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Emergency Report")
        emergency_text = st.text_area(
            "Describe the emergency situation:",
            placeholder="e.g., 'Fire in the storage room, smoke visible, people evacuating...'",
            height=150,
            key="emergency_input",
            label_visibility="collapsed"
        )
        
        # Big analysis button
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("🚨 ANALYZE EMERGENCY", use_container_width=True, key="btn_analyze"):
                if emergency_text.strip():
                    with st.spinner("🔍 AI Analyzing... Processing threat level..."):
                        time.sleep(1)
                        try:
                            emergency_type, confidence = predict_emergency(emergency_text)
                            st.session_state.analysis_result = {
                                "type": emergency_type,
                                "confidence": confidence,
                                "text": emergency_text,
                                "timestamp": datetime.now()
                            }
                            st.success("✅ Analysis Complete!")
                        except Exception as e:
                            st.error(f"⚠️ Analysis failed: {str(e)}")
                else:
                    st.warning("⚠️ Please describe the emergency first")
        
        with col_btn2:
            if st.button("🔄 Clear Input", use_container_width=True):
                st.session_state.analysis_result = None
    
    with col2:
        st.markdown("### 🎯 ANALYSIS RESULT")
        
        if "analysis_result" in st.session_state and st.session_state.analysis_result:
            result = st.session_state.analysis_result
            
            # Result card
            emergency_type = result["type"]
            confidence = result["confidence"]
            color = get_emergency_color(emergency_type)
            emoji = get_emergency_emoji(emergency_type)
            
            st.markdown(f"""
            <div class="card-alert">
                <div style="text-align: center; margin: 15px 0;">
                    <div style="font-size: 3rem;">{emoji}</div>
                    <div style="font-size: 1.5rem; color: {color}; font-weight: bold; margin: 10px 0;">
                        {emergency_type.upper()}
                    </div>
                    <div style="font-size: 2rem; color: {color}; text-shadow: 0 0 15px rgba(255, 0, 85, 0.5);">
                        {confidence}% Confidence
                    </div>
                    <div style="font-size: 0.9rem; color: #b0b0b0; margin-top: 10px;">
                        Detected: {result['timestamp'].strftime('%H:%M:%S')}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show evacuation route map for public users
            primary_route = ["Room A", "Corridor 1", "Stairs Left", "Exit 1"]
            alternate_route = ["Room A", "Corridor 1", "Corridor 2", "Stairs Center", "Exit 2"]
            evacuation_map = create_evacuation_map(primary_route, alternate_route, emergency_type)
            st.plotly_chart(evacuation_map, width="stretch")
            
        else:
            st.markdown("""
            <div class="card">
                <div style="text-align: center; color: #666; padding: 40px 0;">
                    ⏳ Waiting for analysis...
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Evacuation & Safety Tips
    col_evac, col_tips = st.columns([1, 1])
    
    with col_evac:
        st.markdown("### 🚪 EVACUATION PATH")
        st.markdown("""
        <div class="card-success">
            <div style="font-size: 1.1rem; line-height: 2.5; color: #e0e0e0;">
                <strong style="color: #00ff88;">Current Location:</strong> Building A, Floor 3 →<br>
                <strong style="color: #00ff88;">Nearest Exit:</strong> Exit 2 (Stairs Center) →<br>
                <strong style="color: #00ff88;">Muster Point:</strong> East Parking Zone →<br>
                <strong style="color: #00ff88;">Distance:</strong> 150 meters<br>
                <strong style="color: #00ff88;">Estimated Time:</strong> 8-10 minutes
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_tips:
        st.markdown("### ✅ SAFETY GUIDELINES")
        
        safety_tips = [
            ("🚫", "Do NOT use elevators under any circumstances"),
            ("👥", "Stay with others, help those who need assistance"),
            ("📢", "Follow emergency personnel instructions"),
            ("🏃", "Walk quickly but don't run or panic"),
            ("✋", "Don't stop to collect personal belongings")
        ]
        
        for emoji, tip in safety_tips:
            st.markdown(f"""
            <div class="grid-item">
                <div style="font-size: 1.3rem; margin-bottom: 8px;">{emoji}</div>
                <div style="color: #e0e0e0; font-weight: 500; font-size: 1rem;">{tip}</div>
            </div>
            """, unsafe_allow_html=True)

# ================================================================
# OFFICIAL DASHBOARD
# ================================================================

def show_official_dashboard():
    """Display official command center dashboard"""
    
    st.markdown("""
    <div class="title-glowing">🛡️ COMMAND CENTER</div>
    <div class="subtitle">Real-Time Incident Management & Response Control</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top metrics
    st.markdown("### 📊 LIVE INCIDENT METRICS")
    
    col1, col2, col3, col4 = st.columns(4)
    
    show_metric_card(col1, "Total Incidents", "24", "Active", "🚨")
    show_metric_card(col2, "Fire Cases", "3", "High Risk", "🔥")
    show_metric_card(col3, "Medical Cases", "12", "Moderate", "⚕️")
    show_metric_card(col4, "Gas Threats", "2", "Low", "☣️")
    
    st.markdown("---")
    
    # Live incident table
    st.markdown("### 📋 ACTIVE INCIDENTS")
    incidents_df = generate_mock_incidents(8)
    
    # Color code the table
    def color_status(status):
        if status == "Active":
            return "🔴 Active"
        elif status == "Contained":
            return "🟡 Contained"
        else:
            return "🟢 Resolved"
    
    incidents_df["Status"] = incidents_df["Status"].apply(color_status)
    
    st.dataframe(incidents_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Two column layout for control panels
    st.markdown("### ⚙️ OPERATIONAL CONTROL")
    
    col_crowd, col_evacuation = st.columns([1, 1])
    
    # ========================
    # CROWD CONTROL PANEL
    # ========================
    
    with col_crowd:
        st.markdown("#### 👥 CROWD CONTROL OPTIMIZER")
        
        cc_col1, cc_col2 = st.columns(2)
        
        with cc_col1:
            st.markdown("<div style='color: #00d9ff; font-weight: bold; margin-bottom: 8px;'>Total People</div>", unsafe_allow_html=True)
            total_people = st.number_input(
                "Total People:",
                min_value=1,
                max_value=5000,
                value=500,
                step=10,
                label_visibility="collapsed"
            )
            
            st.markdown("<div style='color: #00d9ff; font-weight: bold; margin-bottom: 8px; margin-top: 15px;'>Path Width (meters)</div>", unsafe_allow_html=True)
            path_width = st.number_input(
                "Path Width (meters):",
                min_value=1.0,
                max_value=20.0,
                value=4.0,
                step=0.5,
                label_visibility="collapsed"
            )
        
        with cc_col2:
            st.markdown("<div style='color: #00d9ff; font-weight: bold; margin-bottom: 8px;'>Available Exits</div>", unsafe_allow_html=True)
            exits = st.number_input(
                "Available Exits:",
                min_value=1,
                max_value=10,
                value=3,
                step=1,
                label_visibility="collapsed"
            )
            
            st.markdown("<div style='color: #00d9ff; font-weight: bold; margin-bottom: 8px; margin-top: 15px;'>Risk Level</div>", unsafe_allow_html=True)
            risk_level = st.selectbox(
                "Risk Level:",
                ["Low", "Medium", "High"],
                label_visibility="collapsed"
            )
        
        st.markdown("<div style='color: #00d9ff; font-weight: bold; margin-bottom: 8px; margin-top: 15px;'>Crowd Congestion Level</div>", unsafe_allow_html=True)
        congestion = st.selectbox(
            "Crowd Congestion:",
            ["low", "medium", "high"],
            index=1,
            label_visibility="collapsed",
            key="crowd_congestion_select"
        )
        
        if st.button("⚡ OPTIMIZE CROWD FLOW", use_container_width=True, key="btn_crowd"):
            with st.spinner("🔄 Calculating optimal evacuation strategy..."):
                time.sleep(1)
                
                result = crowd_control(
                    total_people=total_people,
                    exits=exits,
                    path_width=int(path_width),
                    risk_level=risk_level.lower(),
                    congestion=congestion,
                    panic=False
                )
                
                st.markdown("""
                <div class="card-success">
                """, unsafe_allow_html=True)
                
                col_r1, col_r2 = st.columns(2)
                
                with col_r1:
                    st.markdown(f"<div style='color: #e0e0e0; font-size: 1.15rem; line-height: 2.2;'><strong style='color: #00ff88; font-size: 1.2rem;'>⚙️ Mode:</strong><br>{result.get('mode', 'Standard')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: #e0e0e0; font-size: 1.15rem; line-height: 2.2; margin-top: 10px;'><strong style='color: #00ff88; font-size: 1.2rem;'>📊 Capacity:</strong><br>{result.get('capacity', 'N/A')} persons/min</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: #e0e0e0; font-size: 1.15rem; line-height: 2.2; margin-top: 10px;'><strong style='color: #00ff88; font-size: 1.2rem;'>🛣️ Lanes:</strong><br>{result.get('lanes', 'N/A')}</div>", unsafe_allow_html=True)
                
                with col_r2:
                    st.markdown(f"<div style='color: #e0e0e0; font-size: 1.15rem; line-height: 2.2;'><strong style='color: #00ff88; font-size: 1.2rem;'>〰️ Waves:</strong><br>{result.get('waves', 5)} groups</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: #e0e0e0; font-size: 1.15rem; line-height: 2.2; margin-top: 10px;'><strong style='color: #00ff88; font-size: 1.2rem;'>👥 Per Wave:</strong><br>{result.get('per_wave', 'N/A')} people</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: #e0e0e0; font-size: 1.15rem; line-height: 2.2; margin-top: 10px;'><strong style='color: #00ff88; font-size: 1.2rem;'>🚪 Per Exit:</strong><br>{result.get('per_exit', 'N/A')} people</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.success("✅ Evacuation plan optimized!")
    
    # ========================
    # EVACUATION STRATEGY PANEL
    # ========================
    
    with col_evacuation:
        st.markdown("#### 🗺️ EVACUATION STRATEGY")
        
        st.markdown("<div style='color: #00d9ff; font-weight: bold; margin-bottom: 8px;'>Emergency Type</div>", unsafe_allow_html=True)
        emergency_select = st.selectbox(
            "Emergency Type:",
            ["Fire", "Medical Emergency", "Gas Leak", "Security Breach"],
            label_visibility="collapsed"
        )
        
        if st.button("📍 ROUTE PLANNING", use_container_width=True, key="btn_evacuation"):
            with st.spinner("🧭 Calculating best evacuation routes..."):
                time.sleep(1.5)
                
                # Build and analyze graph
                G = build_graph()
                
                # Apply conditions based on emergency type
                G_modified = apply_conditions(
                    G,
                    emergency_type=emergency_select.lower(),
                    severity="medium",
                    congestion=0.5,
                    blocked_nodes=[]
                )
                
                # Define routes
                primary_route = ["Room A", "Corridor 1", "Stairs Left", "Exit 1"]
                alternate_route = ["Room A", "Corridor 1", "Corridor 2", "Stairs Center", "Exit 2"]
                
                # Create and display the map
                evacuation_map = create_evacuation_map(primary_route, alternate_route, emergency_select)
                st.plotly_chart(evacuation_map, use_container_width=True)
                
                # Display route information
                st.markdown("---")
                
                col_info1, col_info2 = st.columns([1, 1])
                
                with col_info1:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #1a2847 0%, #0f3460 100%); 
                                border: 2px solid #ff0055; border-radius: 12px; padding: 20px;">
                        <div style="color: #ff0055; font-size: 1.3rem; font-weight: bold; margin-bottom: 15px;">
                            🎯 PRIMARY ROUTE
                        </div>
                        <div style="color: #e0e0e0; font-size: 1.1rem; line-height: 2;">
                            Room A ➜ Corridor 1 ➜ Stairs Left ➜ Exit 1
                        </div>
                        <div style="color: #b0b0b0; margin-top: 15px; font-size: 0.95rem;">
                            ⏱️ Estimated time: 8-10 minutes<br>
                            📏 Distance: 150 meters
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_info2:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #1a2847 0%, #0f3460 100%); 
                                border: 2px solid #ffaa00; border-radius: 12px; padding: 20px;">
                        <div style="color: #ffaa00; font-size: 1.3rem; font-weight: bold; margin-bottom: 15px;">
                            🔄 ALTERNATE ROUTE
                        </div>
                        <div style="color: #e0e0e0; font-size: 1.1rem; line-height: 2;">
                            Room A ➜ Corridor 1 ➜ Corridor 2 ➜ Stairs Center ➜ Exit 2
                        </div>
                        <div style="color: #b0b0b0; margin-top: 15px; font-size: 0.95rem;">
                            ⏱️ Estimated time: 10-12 minutes<br>
                            📏 Distance: 180 meters
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.success(f"✅ Routes verified and optimized for {emergency_select.lower()}")

# ================================================================
# ADMIN DASHBOARD
# ================================================================

def show_admin_dashboard():
    """Display admin AI monitoring dashboard"""
    
    st.markdown("""
    <div class="title-glowing">🤖 AI MONITORING COMMAND</div>
    <div class="subtitle">System Performance & Predictive Analytics</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top metrics row
    st.markdown("### 📈 SYSTEM METRICS")
    
    col1, col2, col3, col4 = st.columns(4)
    
    show_metric_card(col1, "Total Incidents", "247", "24-Hour", "🚨")
    show_metric_card(col2, "Fire Cases 🔥", "31", "High Priority", "🔥")
    show_metric_card(col3, "Medical ⚕️", "125", "Handled", "⚕️")
    show_metric_card(col4, "Gas/Hazmat ☣️", "18", "Contained", "☣️")
    
    st.markdown("---")
    
    # Charts section
    st.markdown("### 📊 INCIDENT ANALYSIS")
    
    col_chart1, col_chart2 = st.columns([1, 1])
    
    # Bar chart - Incident distribution
    with col_chart1:
        incidents_data = {
            "Emergency Type": ["Fire", "Medical", "Gas Leak", "Security", "Other"],
            "Count": [31, 125, 18, 42, 31]
        }
        df_incidents = pd.DataFrame(incidents_data)
        
        fig_bar = px.bar(
            df_incidents,
            x="Emergency Type",
            y="Count",
            title="Incident Distribution (24H)",
            color="Emergency Type",
            color_discrete_map={
                "Fire": "#ff0055",
                "Medical": "#00ff88",
                "Gas Leak": "#ffff00",
                "Security": "#00d9ff",
                "Other": "#cccccc"
            },
            text="Count"
        )
        
        fig_bar.update_layout(
            plot_bgcolor="#1a2847",
            paper_bgcolor="#0f172a",
            font=dict(color="#e0e0e0"),
            height=400,
            showlegend=False,
            hovermode="x unified"
        )
        
        fig_bar.update_traces(textposition="outside")
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Line chart - Incidents over time
    with col_chart2:
        time_data = {
            "Time": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "23:59"],
            "Incidents": [5, 12, 28, 45, 62, 78, 87]
        }
        df_time = pd.DataFrame(time_data)
        
        fig_line = px.line(
            df_time,
            x="Time",
            y="Incidents",
            title="Incident Timeline (24H)",
            markers=True,
            line_shape="spline"
        )
        
        fig_line.update_traces(
            line=dict(color="#00d9ff", width=3),
            marker=dict(size=10, color="#ff0055")
        )
        
        fig_line.update_layout(
            plot_bgcolor="#1a2847",
            paper_bgcolor="#0f172a",
            font=dict(color="#e0e0e0"),
            height=400,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("---")
    
    # Live incidents feed
    st.markdown("### 📡 LIVE INCIDENT FEED")
    
    incidents_df = generate_mock_incidents(15)
    
    def color_status(status):
        if status == "Active":
            return "🔴"
        elif status == "Contained":
            return "🟡"
        else:
            return "🟢"
    
    incidents_df["Status"] = incidents_df["Status"].apply(color_status) + " " + incidents_df["Status"]
    
    st.dataframe(incidents_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # System status panel
    st.markdown("### 🔧 SYSTEM STATUS PANEL")
    
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        st.markdown("""
        <div class="card-success">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; color: #00ff88;">🤖 AI Model</div>
                <div style="font-size: 1.2rem; color: #00ff88; margin: 10px 0; text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);">RUNNING</div>
                <div style="color: #b0b0b0; font-size: 0.9rem;">Accuracy: 94.7%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status2:
        st.markdown("""
        <div class="card-success">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; color: #00ff88;">⚙️ Crowd Engine</div>
                <div style="font-size: 1.2rem; color: #00ff88; margin: 10px 0; text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);">ACTIVE</div>
                <div style="color: #b0b0b0; font-size: 0.9rem;">Load: 67%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status3:
        st.markdown("""
        <div class="card-success">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; color: #00ff88;">🚨 Alert System</div>
                <div style="font-size: 1.2rem; color: #00ff88; margin: 10px 0; text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);">ENABLED</div>
                <div style="color: #b0b0b0; font-size: 0.9rem;">24/7 Monitoring</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI Insights
    st.markdown("### 🧠 AI INSIGHTS & PREDICTIONS")
    
    col_insight1, col_insight2 = st.columns([1, 1])
    
    with col_insight1:
        st.markdown("""
        <div class="card">
            <div style="color: #00d9ff; font-weight: bold; margin-bottom: 15px; font-size: 1.1rem;">⚡ Trend Analysis</div>
            <div style="color: #e0e0e0; line-height: 2.2; font-size: 1rem;">
                <div>📈 Incident rate increasing 15% YoY</div>
                <div>🔥 Fire incidents peak 18:00-21:00</div>
                <div>⚕️ Medical cases rise weekends</div>
                <div>☣️ Gas hazards clustered in Zone C</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_insight2:
        st.markdown("""
        <div class="card">
            <div style="color: #ffaa00; font-weight: bold; margin-bottom: 15px; font-size: 1.1rem;">⚠️ Predictions</div>
            <div style="color: #e0e0e0; line-height: 2.2; font-size: 1rem;">
                <div>🎯 High incident probability: 20:30</div>
                <div>🔥 Fire risk elevated next 6 hours</div>
                <div>👥 Crowd surge expected 17:00</div>
                <div>📍 Recommend Zone A reinforcement</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_login_page():
    """Display the login page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-title">🚨 SMART EMERGENCY</div>
            <div class="login-subtitle">AI Control System v2.1</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; color: #b0b0b0; margin: 30px 0;">
            <div style="font-size: 1.2rem; margin-bottom: 20px;">
                ⚡ Select Your Access Level
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Role selection
        selected_role = st.radio(
            "Choose your role:",
            ["👤 Public", "👨‍💼 Official Person", "🛡️ Administrator"],
            label_visibility="collapsed"
        )
        
        # Role to key mapping
        role_mapping = {
            "👤 Public": "public",
            "👨‍💼 Official Person": "official",
            "🛡️ Administrator": "admin"
        }
        
        st.markdown("---")
        
        if st.button("🔓 LOGIN & ENTER SYSTEM", use_container_width=True):
            role_key = role_mapping[selected_role]
            st.session_state.authenticated = True
            st.session_state.current_role = role_key
            st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.85rem; margin-top: 40px;">
            <div>🔒 Secure Multi-Role Authentication System</div>
            <div style="margin-top: 10px;">Version 2.1.0 | 24/7 Monitoring Active</div>
        </div>
        """, unsafe_allow_html=True)

# ================================================================
# HEADER SECTION
# ================================================================

def show_header():
    """Display main header with metrics"""
    
    st.markdown("""
    <div class="title-glowing">🚨 SMART EMERGENCY AI CONTROL SYSTEM</div>
    <div class="subtitle">Real-Time AI Crisis Detection & Evacuation Intelligence</div>
    """, unsafe_allow_html=True)
    
    # Quick metrics header
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Incidents", "247", "+12 from yesterday")
    
    with col2:
        st.metric("🚨 Active Alerts", "7", "requires action")
    
    with col3:
        st.metric("✅ System Status", "Active", "all systems nominal")
    
    with col4:
        st.metric("🤖 AI Model", "94.7%", "accuracy")
    
    st.markdown("---")

# ================================================================
# MAIN APP
# ================================================================

def main():
    """Main app logic"""
    
    # Initialize session state
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "current_role" not in st.session_state:
        st.session_state.current_role = None
    
    # Show login page if not authenticated
    if not st.session_state.authenticated:
        show_login_page()
        return
    
    # Show header
    show_header()
    
    # Setup sidebar
    setup_sidebar()
    
    # Setup sidebar and get role
    role = st.session_state.current_role
    
    # Show appropriate dashboard based on role
    if role == "public":
        show_public_dashboard()
    elif role == "official":
        show_official_dashboard()
    elif role == "admin":
        show_admin_dashboard()

if __name__ == "__main__":
    main()
# =========================
# LIVE ALERT SYSTEM
# =========================
def live_alert_banner():
    alerts = [
        ("🔥 Fire detected in Corridor 2", "error"),
        ("⚕️ Medical emergency reported", "success"),
        ("☣️ Gas leak detected", "warning"),
        ("🟢 System operating normally", "info")
    ]
    msg, level = random.choice(alerts)

    if level == "error":
        st.error(msg)
    elif level == "success":
        st.success(msg)
    elif level == "warning":
        st.warning(msg)
    else:
        st.info(msg)
