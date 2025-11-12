# streamlit_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
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
# Layout: Metrics
# -------------------------
st.title("IoT Live Dashboard")
col1, col2, col3 = st.columns(3)
metric1 = col1.metric("Energy Today", "0 kWh")
metric2 = col2.metric("Water Today", "0 L")
metric3 = col3.metric("Lighting", "0%")

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
# Sidebar: AI Optimization
# -------------------------
st.sidebar.header("AI Optimization")
ai_placeholder = st.sidebar.empty()

# -------------------------
# Main loop (Streamlit-friendly)
# -------------------------
refresh_rate = 5  # seconds

while True:
    # Simulate new data
    new_row = simulate_data()
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)

    # Update metrics
    metric1.metric("Energy Today", f"{new_row['Energy']} kWh")
    metric2.metric("Water Today", f"{new_row['Water']} L")
    metric3.metric("Lighting", f"{new_row['Lighting']}%")

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

    # Update AI Optimization
    ai_messages = []
    if new_row['Energy'] > 120:
        ai_messages.append("⚠️ High energy usage! Consider reducing appliances.")
    else:
        ai_messages.append("✅ Energy usage normal.")
    if new_row['Water'] > 80:
        ai_messages.append("⚠️ High water usage! Consider saving water.")
    else:
        ai_messages.append("✅ Water usage normal.")
    if new_row['Lighting'] < 40:
        ai_messages.append("💡 Lighting is low; check brightness.")
    ai_placeholder.markdown("\n".join(ai_messages))

    # Update time
    time_placeholder.markdown(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    time.sleep(refresh_rate)
