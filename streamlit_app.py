import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

st.set_page_config(page_title="IoT Smart Monitoring Dashboard", layout="wide")

# Simulate live data
now = datetime.datetime.now()
energy_today = round(np.random.normal(4500, 100), 2)
water_today = round(np.random.normal(1200, 50), 2)
carbon_savings = round(energy_today * 0.016, 2)  # Approx 0.016 kg CO₂/kWh
energy_last_week_change = -15  # Simulated drop

# Sidebar navigation
tabs = ["Campus Overview", "Energy", "Water", "Alerts", "Sustainability Report"]
selected_tab = st.sidebar.radio("Navigation", tabs)

# Header
st.title("🏫 IoT Smart Monitoring Dashboard")
st.subheader(f"📅 {now.strftime('%B %d, %Y')} 🕒 {now.strftime('%I:%M %p')}")

# Live Statistics
st.markdown("### 🔢 Live Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Energy Usage Today", f"{energy_today} kWh", f"{energy_last_week_change}%")
col2.metric("Water Usage Today", f"{water_today} L")
col3.metric("Carbon Savings", f"{carbon_savings} kg CO₂")
col4.metric("Energy Usage Last Week", "↓ 15%", "-")

# Simulate hourly data
hours = [f"{h}:00" for h in range(0, 13, 2)]
energy_data = np.random.normal(600, 50, len(hours))
water_data = np.random.normal(150, 20, len(hours))

# Energy Trend Graph
st.markdown("### ⚡ Energy Usage Trend")
energy_df = pd.DataFrame({"Time": hours, "Energy (kWh)": energy_data})
st.line_chart(energy_df.set_index("Time"))

# Water Trend Graph
st.markdown("### 🚰 Water Usage Trend")
water_df = pd.DataFrame({"Time": hours, "Water (L)": water_data})
st.bar_chart(water_df.set_index("Time"))

# AI Optimization Alerts
st.markdown("### 🤖 AI Optimization Alerts")
with st.expander("View Alerts"):
    st.warning("Dorm B’s lights remain on between 11 PM–5 AM, wasting 35 kWh/day")
    st.info("Schedule light check near Building 4 – possible leak")

# System Diagnosis
st.markdown("### 🛠️ System Diagnostics")
diag_col1, diag_col2 = st.columns(2)
diag_col1.success("Building 1: Normal")
diag_col2.warning("Building 2: Moderate")

# Ginntrt Central Status
st.markdown("### 🧭 Ginntrt Central Status")
status = ["Normal", "Moderate", "Hazard", "Hot/Temp tip"]
status_colors = {"Normal": "✅", "Moderate": "⚠️", "Hazard": "❌", "Hot/Temp tip": "🔥"}
for s in status:
    st.write(f"{status_colors[s]} {s}")

# Footer
st.markdown("---")
st.caption("Simulated dashboard for campus resource monitoring. Powered by Streamlit.")
