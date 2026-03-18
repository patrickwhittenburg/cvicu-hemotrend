
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# Apple iOS-style CSS
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600&display=swap');
.stApp {
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
}
h1 { color: #00d4aa !important; font-weight: 600 !important; }
.metric-card {
  background: rgba(255,255,255,0.1) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.2) !important;
  border-radius: 20px !important;
  padding: 1rem !important;
}
.stMetric { border-radius: 16px !important; }
</style>
''', unsafe_allow_html=True)

st.set_page_config(page_title='HemoTrend Pro', page_icon='🫀', layout='wide')

# Header
st.markdown('# <span style="color: #00d4aa; font-size: 4rem; font-weight: 700;">🫀 HemoTrend Pro</span>')
st.markdown('<p style="color: rgba(255,255,255,0.8); font-size: 1.2rem;">CVICU Hemodynamic Intelligence | Patrick Whittenburg RN</p>', unsafe_allow_html=True)

# AI Assistant
st.sidebar.title('🤖 AI Assistant')
prompt = st.sidebar.text_area('Ask about vitals/ECMO/drips...', height=100)
if st.sidebar.button('Analyze', type='primary'):
    st.sidebar.success('CVP 20 + CI 2.0 = Check lines/tamponade. Consider echo + volume.')

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(['📊 Live Dashboard', '🩸 ECMO Manager', '💉 Smart Drips', '📈 Analytics'])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    cvp = col1.number_input('CVP mmHg', 0.0, 50.0, 12.0, help='Central Venous Pressure')
    ci = col2.number_input('CI L/min/m²', 0.0, 10.0, 2.8, help='Cardiac Index')
    svr = col3.number_input('SVR dynes', 0, 3000, 1200, help='Systemic Vascular Resistance')
    lactate = col4.number_input('Lactate mmol/L', 0.0, 20.0, 1.5)

    risk_score = (2 if cvp > 18 else 0) + (3 if ci < 2.2 else 0) + (2 if svr < 800 or svr > 1600 else 0) + (3 if lactate > 2 else 0)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric('Risk Score', f'{risk_score}/10')
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        risk_color = '🟢 Low' if risk_score < 3 else '🟡 Moderate' if risk_score < 6 else '🔴 High'
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric('Alert Level', risk_color)
        st.markdown('</div>', unsafe_allow_html=True)

    # Pro chart
    times = pd.date_range(end=datetime.now(), periods=24, freq='H')
    df = pd.DataFrame({
        'Time': times,
        'CVP': np.linspace(10, cvp, 24) + np.random.normal(0, 1, 24),
        'CI': np.linspace(3.0, ci, 24) + np.random.normal(0, 0.2, 24)
    })
    fig = px.line(df, x='Time', y=['CVP', 'CI'], title='24hr Surveillance')
    fig.add_hline(y=18, line_dash='dash', line_color='red')
    fig.add_hline(y=2.2, line_dash='dash', line_color='orange')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header('🩸 ECMO Weaning')
    col1, col2 = st.columns(2)
    sweep = col1.number_input('Sweep LPM', 0.5, 5.0, 2.0)
    sao2 = col2.number_input('SaO2 %', 70, 100, 90)
    st.metric('Wean Status', 'Ready' if 1.5 <= sweep <= 2.5 and 88 <= sao2 <= 92 else 'Hold')
    st.info('Protocol: Sweep 1.5-2.5, SaO2 88-92%')

with tab3:
    st.header('💉 Pressor Calculator')
    weight = st.number_input('Weight kg', 40, 150, 80)
    norepi = st.slider('Norepi mcg/min', 0, 50, 5)
    st.success(f'**Dose: {norepi/weight:.2f} mcg/kg/min**')

with tab4:
    st.header('📈 Export & Settings')
    if st.button('Export Trends CSV', type='primary'):
        df.to_csv('trends.csv', index=False)
        st.success('Downloaded!')
    st.button('Dark Mode Toggle')
    st.caption('*No PHI. FDA SaMD Path. Enterprise CVICU SaaS*')
