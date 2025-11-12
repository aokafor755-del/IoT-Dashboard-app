# streamlit_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import altair as alt

st.set_page_config(page_title="IoT Dashboard", layout="wide")

# -------------------------
# Auto-refresh every 5 seconds
# -------------------------
st_autorefresh = st.experimental_rerun

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

# Add new data point
new_row = simulate_data()
st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)

# Keep only last 20 points for performance
df = st.session_state.data.tail(20)

# -------------------------
# Layout: Metrics
# -------------------------
st.title("IoT Live Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Energy Today", f"{new_row['Energy']} kWh")
col2.metric("Water Today", f"{new_row['Water']} L")
col3.metric("Lighting", f"{new_row['Lighting']}%")

# -------------------------
# System Diagram
# -------------------------
st.subheader("System Diagram")
st.image("https://via.placeholder.com/800x300.png?text=System+Diagram", use_column_width=True)

# -------------------------
# Energy & Water Trend Graphs
# -------------------------
st.subheader("Energy & Water Trends")
chart = alt.Chart(df).transform_fold(
    ["Energy", "Water"], as_=["Metric", "Value"]
).mark_line(point=True).encode(
    x="Time",
    y="Value",
    color="Metric"
).properties(height=300)
st.altair_chart(chart, use_container_width=True)

# -------------------------
# Time & Date
# -------------------------
st.markdown(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# -------------------------
# Sidebar: AI Optimization
# -------------------------
st.sidebar.header("AI Optimization")
ai_messages = []
if new_row['Energy'] > 120:
    ai_messages.append("⚠️ High energy usage! Reduce appliances.")
else:
    ai_messages.append("✅ Energy usage normal.")
if new_row['Water'] > 80:
    ai_messages.append("⚠️ High water usage! Save water.")
else:
    ai_messages.append("✅ Water usage normal.")
if new_row['Lighting'] < 40:
    ai_messages.append("💡 Lighting is low; check brightness.")
st.sidebar.markdown("\n".join(ai_messages))

# -------------------------
# Auto-refresh every 5 seconds
# -------------------------
st.experimental_rerun()
