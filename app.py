import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title='CVICU HemoTrend Pro', page_icon='🫀', layout='wide')
st.title('🫀 CVICU HemoTrend Pro 2.0')
st.markdown('*Advanced Hemodynamic Intelligence | Patrick Whittenburg RN*')

tab1, tab2, tab3, tab4 = st.tabs(['📊 Dashboard', '🩸 ECMO', '💉 Drips', '⚙️ Settings'])

with tab1:
    col1, col2, col3 = st.columns(3)
    cvp = col1.number_input('CVP (mmHg)', 0.0, 50.0, 12.0)
    ci = col2.number_input('Cardiac Index', 0.0, 10.0, 2.8)
    svr = col3.number_input('SVR', 0, 3000, 1200)

    risk_score = sum([2 if cvp > 18 else 0, 3 if ci < 2.2 else 0, 2 if svr < 800 or svr > 1600 else 0])
    risk_level = '🟢 Low' if risk_score < 3 else '🟡 Moderate' if risk_score < 6 else '🔴 High'

    col1, col2, col3 = st.columns(3)
    col1.metric('Risk Score', f'{risk_score}/10')
    col2.metric('Risk Level', risk_level)
    col3.metric('Stability', '87%', '+3%')

    times = pd.date_range(end=datetime.now(), periods=24, freq='H')
    df = pd.DataFrame({
        'Time': times,
        'CVP': np.linspace(10, cvp, 24) + np.random.normal(0, 1, 24),
        'CI': np.linspace(3.0, ci, 24) + np.random.normal(0, 0.2, 24),
        'SVR': np.linspace(1200, svr, 24) + np.random.normal(0, 50, 24)
    })

    fig = px.line(df, x='Time', y=['CVP', 'CI', 'SVR'], title='24hr Hemodynamic Trends')
    fig.add_hline(y=18, line_dash='dash', line_color='red', annotation_text='CVP Alert')
    fig.add_hline(y=2.2, line_dash='dash', line_color='orange', annotation_text='CI Threshold')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header('ECMO Weaning')
    st.metric('Sweep Goal', '2.0 LPM', 'Optimal')
    st.metric('SaO2 Target', '88-92%', 'Good')
    st.info('Protocol: Sweep 1.5-2.5, SaO2 88-92%, lactate <2')

with tab3:
    st.header('Pressor Titration')
    weight = st.number_input('Weight (kg)', 40, 150, 80)
    norepi = st.slider('Norepi mcg/m
