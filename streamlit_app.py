import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Page setup
st.set_page_config(page_title="IoT Smart Monitoring Dashboard", layout="wide")

# Simulated live data
def simulate_data():
    now = datetime.datetime.now()
    hours = [f"{h}:00" for h in range(0, 24, 2)]
    energy_data = np.random.normal(loc=500, scale=50, size=len(hours)).round(2)
    water_data = np.random.normal(loc=100, scale=20, size=len(hours)).round(2)
    return now, hours, energy_data, water_data

now, hours, energy_data, water_data = simulate_data()

# Header
st.title("🏫 IoT Smart Monitoring Dashboard")
st.markdown(f"**Date:** {now.strftime('%A, %d %B %Y')} &nbsp;&nbsp; **Time:** {now.strftime('%I:%M %p')}")

# Live Metrics
st.markdown("### 🔢 Live Statistics")
energy_today = energy_data.sum().round(2)
water_today = water_data.sum().round(2)
carbon_savings = round(energy_today * 0.016, 2)
energy_last_week_change = -15  # Simulated

col1, col2, col3, col4 = st.columns(4)
col1.metric("Energy Usage Today", f"{energy_today} kWh", f"{energy_last_week_change}%")
col2.metric("Water Usage Today", f"{water_today} L")
col3.metric("Carbon Savings", f"{carbon_savings} kg CO₂")
col4.metric("Energy Usage Last Week", "↓ 15%", "-")

# Charts
st.markdown("### ⚡ Energy Usage Trend")
energy_df = pd.DataFrame({"Time": hours, "Energy (kWh)": energy_data})
st.line_chart(energy_df.set_index("Time"))

st.markdown("### 🚰 Water Usage Trend")
water_df = pd.DataFrame({"Time": hours, "Water (L)": water_data})
st.bar_chart(water_df.set_index("Time"))

# AI Optimization Alerts
st.markdown("### 🤖 AI Optimization Alerts")
with st.expander("View Alerts"):
    st.warning("Dorm B’s lights remain on between 11 PM–5 AM, wasting
