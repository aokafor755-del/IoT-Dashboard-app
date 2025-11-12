# streamlit_dashboard_final.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import plotly.graph_objects as go
# ============================
# CONFIG
# ============================
CSV_FILE = "iot_streamlit_data.csv"
MAX_POINTS = 600
UPDATE_INTERVAL = 5  # seconds
st.set_page_config(page_title="IoT Dashboard", layout="wide", initial_sidebar_state="expanded")

# ============================
# STYLES (Dark Mode like PyQt)
# ============================
st.markdown("""
<style>
.main {background-color: #0F1720; color: #DDE6ED;}
.stButton>button {background-color:#1E90FF; color:white;}
h1, h2, h3, h4, h5, h6 {color:#DDE6ED;}
.stMetric-label, .stMetric-value {color:#DDE6ED;}
div[data-testid="stSidebar"] {background-color:#0F1720; color:#DDE6ED;}
</style>
""", unsafe_allow_html=True)

# ============================
# DATA INIT + SIMULATION
# ============================
def seed_initial_data(rows=120):
    now = datetime.datetime.now()
    times = [now - datetime.timedelta(seconds=(rows - i - 1)*UPDATE_INTERVAL) for i in range(rows)]
    np.random.seed(42)
    energy = np.clip(np.random.normal(300, 80, rows).cumsum()/10 + 150, 50, 700).round().astype(int)
    water = np.clip(np.random.normal(80, 25, rows).cumsum()/10 + 400, 50, 1500).round().astype(int)
    live = np.clip(np.random.normal(0.2, 0.5, rows).cumsum()/10 + 70, 10, 100).round(1)
    lights_pct = np.clip(20 + 10*np.sin(np.linspace(0,6.28,rows)) + np.random.randn(rows)*3, 0, 100).round(1)
    return pd.DataFrame({"timestamp": times, "energy": energy, "water": water, "live": live, "lights_pct": lights_pct})

if os.path.exists(CSV_FILE):
    try:
        df_master = pd.read_csv(CSV_FILE, parse_dates=["timestamp"])
    except:
        df_master = seed_initial_data()
else:
    df_master = seed_initial_data()
    df_master.to_csv(CSV_FILE, index=False)

def append_simulated_row(df):
    last = df.iloc[-1]
    now = datetime.datetime.now()
    energy = int(max(10, last["energy"] + np.random.randint(-15, 30)))
    water = int(max(5, last["water"] + np.random.randint(-20, 40)))
    live = float(np.clip(last["live"] + np.random.normal(0, 0.6), 10, 100))
    lights_pct = float(np.clip(last["lights_pct"] + np.random.normal(0, 2.5), 0, 100))
    new_row = {"timestamp": now, "energy": energy, "water": water, "live": round(live,1), "lights_pct": round(lights_pct,1)}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    if len(df) > MAX_POINTS: df = df.iloc[-MAX_POINTS:].copy()
    df.to_csv(CSV_FILE, index=False)
    return df

def analyze_for_insights(df):
    insights=[]
    if df.empty: return insights
    last = df.iloc[-1]
    mean_energy = df["energy"].tail(60).mean()
    if last["energy"] > mean_energy * 1.35:
        insights.append(f"INFO: Sudden energy increase: {last['energy']} kWh (mean ~{int(mean_energy)})")
    last_hour = df.tail(12)
    if last["water"] > last_hour["water"].mean() + 2*last_hour["water"].std():
        insights.append("ALERT: Water spike detected — possible leak")
    overnight = df.tail(60)
    overnight = overnight[overnight["timestamp"].dt.hour.isin([23,0,1,2,3,4,5])]
    if not overnight.empty and overnight["lights_pct"].mean() > 40:
        insights.append("WARNING: Lights remain on overnight — estimated waste")
    if last["live"] < 30:
        insights.append("NOTE: Live metric below 30 — consider engagement program")
    if not insights: insights.append("OK: System operating within expected ranges")
    return insights

# ============================
# SIDEBAR
# ============================
st.sidebar.title("Controls")
if st.sidebar.button("Reset Data"):
    df_master = seed_initial_data()
    df_master.to_csv(CSV_FILE, index=False)
    st.sidebar.success("Data reset!")
st.sidebar.download_button("Download CSV", df_master.to_csv(index=False), "iot_data.csv", "text/csv")

# ============================
# HEADER & TOP METRICS
# ============================
st.markdown("## IoT Smart Monitoring Dashboard")
df_master = append_simulated_row(df_master)
last = df_master.iloc[-1]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Live %", f"{last['live']}%")
col2.metric("Energy Today", f"{int(df_master['energy'].tail(24).sum())} kWh")
col3.metric("Water Today", f"{int(df_master['water'].tail(24).sum())} L")
col4.metric("Lights %", f"{last['lights_pct']}%")

# ============================
# PANEL FUNCTIONS
# ============================
def left_panel_content():
    st.markdown("### Live Statistics")
    st.text(f"Energy Today: {int(df_master['energy'].tail(24).sum())} kWh")
    st.text(f"Water Today: {int(df_master['water'].tail(24).sum())} L")
    st.text(f"Live %: {last['live']}%")
    st.text(f"Lights %: {last['lights_pct']}%")
    if st.button("Export CSV"):
        st.download_button("Download CSV", df_master.to_csv(index=False), "iot_data.csv", "text/csv")
    if st.button("Reset Panel Data"):
        df_master = seed_initial_data()
        df_master.to_csv(CSV_FILE, index=False)

def center_panel_content():
    st.markdown("### Energy Trend (kWh)")
    st.line_chart(df_master.set_index("timestamp")["energy"])
    st.markdown("### Water Trend (L)")
    st.line_chart(df_master.set_index("timestamp")["water"])

def right_panel_content():
    st.markdown("### AI Optimization Insights")
    for i in analyze_for_insights(df_master):
        st.write("-", i)
    st.markdown("### System Diagram")
    nodes = [
        {"name": "Building 1", "x":0.1, "y":0.6, "color":"#00CC96"},
        {"name": "Building 2", "x":0.35, "y":0.25, "color":"#00CC96"},
        {"name": "Building 3", "x":0.6, "y":0.6, "color":"#F6C85F"},
        {"name": "Building 4", "x":0.85, "y":0.7, "color":"#FF6B6B"},
        {"name": "Control", "x":0.35, "y":0.8, "color":"#00CC96"}
    ]
    edges = [(0,1),(1,2),(2,3),(0,4)]
    fig = go.Figure()
    for node in nodes:
        fig.add_trace(go.Scatter(
            x=[node["x"]], y=[node["y"]],
            mode='markers+text',
            marker=dict(size=30,color=node["color"]),
            text=[node["name"]],
            textposition="bottom center",
            hoverinfo='text'))
    for a,b in edges:
        fig.add_trace(go.Scatter(
            x=[nodes[a]["x"], nodes[b]["x"]],
            y=[nodes[a]["y"], nodes[b]["y"]],
            mode='lines', line=dict(color='#6A7D8B', width=3),
            hoverinfo='none'))
    fig.update_layout(
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False),
        plot_bgcolor="#0F1720",
        paper_bgcolor="#0F1720",
        margin=dict(l=20,r=20,t=20,b=20))
    st.plotly_chart(fig, use_container_width=True)

# ============================
# DRAG-AND-DROP PANELS
# ============================
panels = [
    {"id": "left", "title": "Live Stats", "content": left_panel_content},
    {"id": "center", "title": "Energy/Water Trends", "content": center_panel_content},
    {"id": "right", "title": "AI + System Diagram", "content": right_panel_content},
]

st.markdown("### 🧩 Drag Panels to Reorder")
# Dashboard main metrics section
st.write("🔹 Live Statistics")

col1, col2, col3 = st.columns(3)
with col1:
with col1:
    st.metric("Energy Today", f"{energy_today} kWh")

with col2:
    st.metric("Water Today", f"{water_today} L")

with col3:
    st.metric("Lighting", f"{lighting}%")
