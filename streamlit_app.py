# streamlit_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import altair as alt

st.set_page_config(page_title="IoT Dashboard", layout="wide")

# -------------------------
# Initialize data storage
# -------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Energy", "Water", "Lighting"])

# -------------------------
# Function to simulate sensors
# -------------------------
def simulate_data():
    now = datetime.now().strftime("%H:%M:%S")
    energy = np.random.randint(50, 150)  # kWh
    water = np.random.randint(20, 100)   # Liters
    lighting = np.random.randint(30, 100)  # %
    return {"Time": now, "Energy": energy, "Water": water, "Lighting": lighting}

# -------------------------
# Sidebar: AI Optimization
# -------------------------
st.sidebar.header("AI Optimization")
latest_data = st.session_state.data.tail(1)
if not latest_data.empty:
    energy = latest_data["Energy"].values[0]
    water = latest_data["Water"].values[0]
    lighting = latest_data["Lighting"].values[0]
    if energy > 120:
        st.sidebar.warning("High energy usage! Consider reducing appliance use.")
    else:
        st.sidebar.success("Energy usage is normal.")
    if water > 80:
        st.sidebar.warning("High water usage! Consider saving water.")
    else:
        st.sidebar.success("Water usage is normal.")
    if lighting < 40:
        st.sidebar.info("Lighting is low; check brightness levels.")

# -------------------------
# Layout: Metrics
# -------------------------
st.title("IoT Live Dashboard")
col1, col2, col3 = st.columns(3)

if not latest_data.empty:
    col1.metric("Energy Today", f"{energy} kWh")
    col2.metric("Water Today", f"{water} L")
    col3.metric("Lighting", f"{lighting}%")
else:
    col1.metric("Energy Today", "0 kWh")
    col2.metric("Water Today", "0 L")
    col3.metric("Lighting", "0%")

# -------------------------
# System Diagram Placeholder
# -------------------------
st.subheader("System Diagram")
st.image("https://via.placeholder.com/800x300.png?text=System+Diagram", use_column_width=True)

# -------------------------
# Energy & Water Trend Graphs
# -------------------------
st.subheader("Energy & Water Trends")
chart_placeholder = st.empty()

# -------------------------
# Time & Date
# -------------------------
time_placeholder = st.empty()

# -------------------------
# Main loop
# -------------------------
while True:
    # Simulate new data
    new_row = simulate_data()
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
    
    # Update metrics
    col1.metric("Energy Today", f"{new_row['Energy']} kWh")
    col2.metric("Water Today", f"{new_row['Water']} L")
    col3.metric("Lighting", f"{new_row['Lighting']}%")
    
    # Update chart
    df = st.session_state.data.copy()
    df = df.tail(20)  # last 20 points
    chart = alt.Chart(df).transform_fold(
        ["Energy", "Water"], as_=["Metric", "Value"]
    ).mark_line(point=True).encode(
        x="Time",
        y="Value",
        color="Metric"
    ).properties(height=300)
    chart_placeholder.altair_chart(chart, use_container_width=True)
    
    # Update time
    time_placeholder.markdown(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    time.sleep(5)           
