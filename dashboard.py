import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import time
from config import DB_CONFIG, TABLE_NAME

# PAGE CONFIGURATION
st.set_page_config(
    page_title="IoT Fleet Monitor",
    page_icon="🚛",
    layout="wide"
)

# TITLE
st.title("🚛 Real-Time IoT Fleet Telemetry & Predictive Maintenance")

# AUTO-REFRESH LOGIC
# This forces the app to reload every 2 seconds to show live data
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = time.time()

def load_data():
    """
    Fetches the latest data for all trucks from Postgres.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    query = f"""
        SELECT * FROM {TABLE_NAME}
        ORDER BY timestamp DESC
        LIMIT 500
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# LOAD DATA
df = load_data()

# LAYOUT: TOP METRICS
# We create 3 columns to show high-level stats (The "Manager View")
kpi1, kpi2, kpi3 = st.columns(3)

active_trucks = df['truck_id'].nunique()
avg_temp = df['engine_temp_c'].mean()
critical_alerts = df[df['status'] == 'OVERHEAT_WARNING'].shape[0]

kpi1.metric("Active Trucks", active_trucks)
kpi2.metric("Fleet Avg Temp", f"{avg_temp:.1f} °C")
kpi3.metric("Critical Alerts", critical_alerts, delta_color="inverse")

st.divider()

# LAYOUT: CHARTS
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Live Fleet Location")
    # Streamlit has a built-in map function that looks for 'lat'/'lon' columns
    # We rename our columns to match what Streamlit expects
    map_data = df.rename(columns={"gps_lat": "lat", "gps_long": "lon"})
    st.map(map_data)

with col2:
    st.subheader("📈 Engine Temperature Trends")
    # Using Plotly for an interactive line chart
    fig = px.line(df, x='timestamp', y='engine_temp_c', color='truck_id',
                  title="Real-Time Engine Telemetry")
    st.plotly_chart(fig, use_container_width=True)

# RAW DATA TABLE (Bottom of page)
with st.expander("View Raw Sensor Data"):
    st.dataframe(df)

# REFRESH BUTTON (Manual refresh + Auto-loop hint)
if st.button('Refresh Data'):
    st.rerun()

# AUTOMATIC RERUN (Simple hack for live dashboard)
time.sleep(2)
st.rerun()