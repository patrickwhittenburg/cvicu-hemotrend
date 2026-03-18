import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# Modern CSS
st.markdown("""
<style>
    .main {background-color: #0e1117}
    .stMetric > label {color: white !important}
    .stMetric > div > div {color: #00d4aa !important}
    .sidebar .sidebar-content {background-color: #1a1d2e}
    h1 {color: #00d4aa !important; font-size: 3rem !important}
    .stPlotlyChart {border-radius: 12px !important}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🫀 **CVICU HemoTrend Pro 2.0**")
st.markdown("*Advanced Hemodynamic Intelligence | Patrick Whittenburg RN*")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🩸 ECMO", "💉 Drips", "⚙️ Settings"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        cvp = st.number_input("CVP", 0.0, 50.0, 12.0, help="Central Venous Pressure")
    with col2:
        ci = st.number_input("CI", 0.0, 10.0, 2.8, help="Cardiac Index")
    with col3:
        svr = st.number_input("SVR", 0, 3000, 1200, help="Systemic Vascular Resistance")

    # Multi-metric cards
    col1, col2, col3, col4 = st.columns(4)
    risk_score = sum([cvp>18, ci<2.2*1.5, svr<800 or svr>1600, 0])
    col1.metric("Risk", f"{risk_score}/10", "↑2")
    col2.metric("Stability", "87%", "+3%")
    col3.metric("Alert", "Tamponade Risk", "High")
    col4.metric("Next Action", "Volume Challenge", "")

    # Advanced chart with thresholds
    times = pd.date_range(end=datetime.now(), periods=24, freq='H')
    df = pd.DataFrame({
        'Time': times,
        'CVP': np.linspace(10, cvp, 24) + np.random.normal(0, 1, 24),
        'CI': np.linspace(3.0, ci, 24) + np.random.normal(0, 0.2, 24)
    })
    fig = px.line(df, x='Time', y=['CVP', 'CI'], 
                  title="24hr Hemodynamic Surveillance",
                  color_discrete_sequence=['#00d4aa', '#ff6b6b'])
    fig.add_hline(y=18, line_dash="dash
