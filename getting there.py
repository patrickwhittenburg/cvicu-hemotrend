
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# Premium Apple UI + Medical Background
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@200;300;400;500;600;700&display=swap');
.stApp {
  background: linear-gradient(135deg, #0a0a0f 0%, #1e1e2f 50%, #0f1620 100%);
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(120,119,198,0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,119,198,0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120,219,255,0.3) 0%, transparent 50%);
}
h1 { 
  color: #00d4aa !important; 
  font-weight: 600 !important; 
  text-shadow: 0 0 20px rgba(0,212,170,0.5);
  font-size: 3.5rem !important;
}
.card {
  background: rgba(255,255,255,0.08) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  border-radius: 24px !important;
  padding: 2rem !important;
  box-shadow: 0 20px 40px rgba(0,0,0,0.3) !important;
}
.stMetric { border-radius: 16px !important; }
.ai-chat { height: 400px !important; }
</style>
''', unsafe_allow_html=True)

st.set_page_config(page_title='HemoTrend Pro v4', page_icon='🫀', layout='wide')

# Header
st.markdown('# <span style="color: #00d4aa; font-size: 4rem; font-weight: 700;">🫀 HemoTrend Pro v4</span>')
st.markdown('<p style="color: rgba(255,255,255,0.9); font-size: 1.4rem; font-weight: 400;">AI‑Powered CVICU Intelligence | Patrick Whittenburg RN</p>', unsafe_allow_html=True)

# AI Assistant - Full Grok‑style
st.sidebar.title('🤖 CVICU AI Assistant')
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.sidebar.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.sidebar.chat_input('Ask about vitals, ECMO, drips, protocols...'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.sidebar.chat_message('user'):
        st.markdown(prompt)

    # Grok‑level responses (rule‑based + CVICU knowledge)
    responses = {
        'cvp': 'CVP 18+ suggests volume overload or tamponade. Check echo, consider diuresis.',
        'ci': 'CI <2.2 = low output. Inotropes (dobutamine/milrinone) or IABP.',
        'ecmo': 'ECMO weaning: Sweep 1.5-2.5 LPM, SaO2 88-92%, lactate <2.',
        'norepi': 'Norepi mcg/kg/min = total mcg/min ÷ weight. Target MAP 65.',
        'swan': 'Swan troubleshooting: Zero at RA level, check damping (sq wave test).'
    }

    response = 'Analyzing...' 
    for key in responses:
        if key in prompt.lower():
            response = responses[key]
            break
    else:
        response = 'CVICU pro tip: Always verify trends with clinical judgment. What vitals?'

    st.session_state.messages.append({'role': 'assistant', 'content': response})
    with st.sidebar.chat_message('assistant'):
        st.markdown(response)

# Main app - Polished dashboard
col1, col2 = st.columns([1,3])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header('📊 Live Vitals')
    cvp = st.number_input('CVP mmHg', 0.0, 50.0, 12.0)
    ci = st.number_input('CI L/min/m²', 0.0, 10.0, 2.8)
    svr = st.number_input('SVR dynes', 0, 3000, 1200)
    lactate = st.number_input('Lactate', 0.0, 20.0, 1.5)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    risk_score = (2 if cvp > 18 else 0) + (3 if ci < 2.2 else 0) + (2 if svr < 800 or svr > 1600 else 0) + (3 if lactate > 2 else 0)
    col1, col2 = st.columns(2)
    col1.metric('Risk Score', f'{risk_score}/10')
    col2.metric('Stability', f'{95-risk_score*2:.0f}%')
    st.markdown('</div>', unsafe_allow_html=True)

# Pro trends chart
st.markdown('<div class="card">', unsafe_allow_html=True)
times = pd.date_range(end=datetime.now(), periods=24, freq='H')
df = pd.DataFrame({
    'Time': times,
    'CVP': np.linspace(10, cvp, 24) + np.random.normal(0, 1, 24),
    'CI': np.linspace(3.0, ci, 24) + np.random.normal(0, 0.2, 24),
    'SVR': np.linspace(1200, svr, 24) + np.random.normal(0, 50, 24)
})
fig = px.line(df, x='Time', y=['CVP', 'CI', 'SVR'], title='24hr CVICU Surveillance')
fig.add_hline(y=18, line_dash='dash', line_color='#ff4757', annotation_text='CVP Alert')
fig.add_hline(y=2.2, line_dash='dash', line_color='#ffa502', annotation_text='CI Threshold')
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Quick tools
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    weight = st.number_input('Weight kg', 40.0, 150.0, 80.0)
    norepi = st.number_input('Norepi mcg/min', 0.0, 50.0, 5.0)
    st.success(f'{norepi/weight:.2f} mcg/kg/min')
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('---')
st.caption('*No PHI | FDA SaMD Path | Enterprise CVICU Platform v4.0*')
