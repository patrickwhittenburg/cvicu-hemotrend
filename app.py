
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="CVICU HemoTrend Pro", page_icon="🫀", layout="wide")
st.title("🫀 CVICU HemoTrend Pro")
st.markdown("**Real-time Hemodynamic Optimizer | Prototype MVP**")

# Sidebar
st.sidebar.header("Vitals")
cvp = st.sidebar.number_input("CVP (mmHg)", 0.0, 50.0, 12.0)
ci = st.sidebar.number_input("Cardiac Index", 0.0, 10.0, 2.8)
svr = st.sidebar.number_input("SVR", 0, 3000, 1200)
lap = st.sidebar.number_input("Lactate", 0.0, 20.0, 1.5)

# Trends
times = pd.date_range(end=datetime.now(), periods=8, freq='H')
cvp_trend = np.linspace(12, cvp, 8) + np.random.normal(0, 0.5, 8)
ci_trend = np.linspace(2.8, ci, 8) + np.random.normal(0, 0.1, 8)
svr_trend = np.linspace(1200, svr, 8) + np.random.normal(0, 50, 8)
df = pd.DataFrame({'Time': times, 'CVP': cvp_trend, 'CI': ci_trend, 'SVR': svr_trend})

# Risk
risk_score = sum([2 if cvp > 18 else 0, 3 if ci < 2.2 else 0, 2 if svr < 800 or svr > 1600 else 0, 3 if lap > 2 else 0])
risk_level = "🟢 Low" if risk_score < 3 else "🟡 Moderate" if risk_score < 6 else "🔴 High"

col1, col2 = st.columns(2)
col1.metric("Risk Score", f"{risk_score}/10")
col2.metric("Risk Level", risk_level)

fig = px.line(df, x='Time', y=['CVP', 'CI', 'SVR'], title="Hemodynamic Trends")
st.plotly_chart(fig, use_container_width=True)

st.caption("*No PHI. Nurse-built prototype. Verify outputs.*")
