import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Page configuration
st.set_page_config(page_title="IoT Smart Monitoring Dashboard", layout="wide")

# ---------- Data Simulation ----------
def simulate_data():
    now = datetime.datetime.now()
    hours = [f"{h}:00" for h in range(0, 24, 2)]
    energy_data = np.random.normal(loc=500, scale=50, size=len(hours)).round(2)
    water_data = np.random.normal(loc=100, scale=20, size=len(hours)).round(2)
    return now, hours, energy_data, water_data

# ---------- Metrics Section ----------
def render_metrics(energy_data, water_data):
    energy_today = energy_data.sum().round(2)
    water_today = water_data.sum().round(2)
    carbon_savings = round(energy_today * 0.016, 2)
    energy_last_week_change = -15  # Simulated

    st.markdown("### 🔢 Live Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⚡ Energy Usage Today", f"{energy_today} kWh", f"{energy_last_week_change}%")
    col2.metric("🚰 Water Usage Today", f"{water_today} L")
    col3.metric("🌱 Carbon Savings", f"{carbon_savings} kg CO₂")
    col4.metric("📉 Energy Usage Last Week", "↓ 15%", "-")

# ---------- Charts Section ----------
def render_charts(hours, energy_data, water_data):
    st.markdown("### 📈 Energy Usage Trend")
    energy_df = pd.DataFrame({"Time": hours, "Energy (kWh)": energy_data})
    st.line_chart(energy_df.set_index("Time"))

    st.markdown("### 📊 Water Usage Trend")
    water_df = pd.DataFrame({"Time": hours, "Water (L)": water_data})
    st.bar_chart(water_df.set_index("Time"))

# ---------- Alerts Section ----------
def render_alerts():
    st.markdown("### 🤖 AI Optimization Alerts")
    with st.expander("View Alerts"):
        st.warning("Dorm B’s lights remain on between 11 PM–5 AM, wasting 35 kWh/day")
        st.info("Schedule light check near Building 4 – possible leak")

# ---------- Diagnostics Section ----------
def render_diagnostics():
    st.markdown("### 🛠️ System Diagnostics")
    diag_col1, diag_col2 = st.columns(2)
    diag_col1.success("🏢 Building 1: Normal")
    diag_col2.warning("🏢 Building 2: Moderate")

# ---------- Ginntrt Central Status ----------
def render_status():
    st.markdown("### 🧭 Ginntrt Central Status")
    status = ["Normal", "Moderate", "Hazard", "Hot/Temp tip"]
    status_icons = {"Normal": "✅", "Moderate": "⚠️", "Hazard": "❌", "Hot/Temp tip": "🔥"}
    for s in status:
        st.write(f"{status_icons[s]} {s}")

# ---------- Main Dashboard ----------
def main():
    st.sidebar.title("Navigation")
    tabs = ["Campus Overview", "Energy", "Water", "Alerts", "Sustainability Report"]
    selected_tab = st.sidebar.radio("Go to", tabs)

    st.title("🏫 IoT Smart Monitoring Dashboard")
    refresh = st.button("🔄 Refresh Data")

    if refresh or 'data' not in st.session_state:
        now, hours, energy_data, water_data = simulate_data()
        st.session_state.data = (now, hours, energy_data, water_data)
    else:
        now, hours, energy_data, water_data = st.session_state.data

    st.markdown(f"**Date:** {now.strftime('%A, %d %B %Y')} &nbsp;&nbsp; **Time:** {now.strftime('%I:%M %p')}")

    if selected_tab == "Campus Overview":
        render_metrics(energy_data, water_data)
        render_charts(hours, energy_data, water_data)
        render_alerts()
        render_diagnostics()
        render_status()
    elif selected_tab == "Energy":
        render_metrics(energy_data, water_data)
        render_charts(hours, energy_data, water_data)
    elif selected_tab == "Water":
        render_charts(hours, energy_data, water_data)
    elif selected_tab == "Alerts":
        render_alerts()
    elif selected_tab == "Sustainability Report":
        render_metrics(energy_data, water_data)
        render_status()

    st.markdown("---")
    st.caption("Simulated dashboard for campus resource monitoring. Built with ❤️ using Streamlit.")

main()
