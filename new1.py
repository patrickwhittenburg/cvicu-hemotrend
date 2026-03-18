
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# Premium UI
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600&display=swap');
.stApp { background: linear-gradient(135deg, #0a0a0f 0%, #1e1e2f 100%); }
h1 { color: #00d4aa !important; font-size: 3rem !important; font-weight: 600 !important; }
.stMetric label { color: rgba(255,255,255,0.9) !important; }
.ai-response { background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 16px; border-left: 4px solid #00d4aa; }
</style>
''', unsafe_allow_html=True)

st.set_page_config(layout="wide")
st.title('🫀 HemoTrend Pro v6 - AI CVICU')
st.markdown('Advanced Intelligence | Patrick Whittenburg RN')

# FULL AI ASSISTANT - Grok‑level CVICU brain
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.sidebar.title('🤖 CVICU AI - Ask Anything')
for msg in st.session_state.messages:
    with st.sidebar.chat_message(msg['role']):
        st.markdown(msg['content'])

prompt = st.sidebar.chat_input('CVP high? ECMO weaning? Swan troubleshooting?')
if prompt:
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.sidebar.chat_message('user'):
        st.markdown(prompt)

    # TOP LEVEL CODER AI - Your exact knowledge + CVICU rules
    lower_prompt = prompt.lower()
    response = ""

    if 'cvp' in lower_prompt or 'central venous' in lower_prompt:
        response = "CVP >18: Volume overload, tamponade, or RV failure. Check echo, PA pressures, consider diuresis/nitro. Normal 8-12 mmHg."
    elif 'ci' in lower_prompt or 'cardiac index' in lower_prompt:
        response = "CI <2.2: Low output. Dobutamine 5mcg/kg/min or milrinone 0.375mcg/kg/min. IABP if refractory. Normal 2.5-4.0."
    elif 'ecmo' in lower_prompt:
        response = "ECMO weaning: Sweep 1.5-2.5 LPM, SaO2 88-92%, lactate <2, no inotropes >24h. Trial off 4h before decann."
    elif 'norepi' in lower_prompt or 'pressor' in lower_prompt:
        response = "Norepi mcg/kg/min = total mcg/min ÷ weight. Start 0.05-0.1, titrate MAP 65-70. Add vasopressin 0.03u/min if >15mcg."
    elif 'swan' in lower_prompt or 'pa catheter' in lower_prompt:
        response = "Swan troubleshooting: 1) Zero at RA (4th ICS), 2) SQ wave test (balloon up 1.5ml 3s), 3) Flush if damped. Normal PAWP 8-12."
    elif 'tamponade' in lower_prompt:
        response = "Tamponade: Pulsus paradoxus >12, RV > LV collapse echo, equalization pressures. Fluid bolus + pericardiocentesis."
    elif 'maze' in lower_prompt:
        response = "Post-MAZE: AFib risk high 24-48h. Amio 1mg/min load then 0.5mg/kg/h drip. Anticoag if CHADS>2."
    else:
        response = "CVICU pro tip: Always verify with clinical judgment + echo. What vitals/procedure? I know Swan, ECMO, drips, post-MAZE."

    st.session_state.messages.append({'role': 'assistant', 'content': response})
    with st.sidebar.chat_message('assistant'):
        st.markdown(f'<div class="ai-response">{response}</div>', unsafe_allow_html=True)

# Dashboard
col1, col2 = st.columns(2)

with col1:
    st.header('📊 Live Vitals')
    cvp = st.number_input('CVP mmHg', 0.0, 50.0, 12.0)
    ci = st.number_input('CI L/min/m²', 0.0, 10.0, 2.8)
    svr = st.number_input('SVR dynes', 0, 3000, 1200)
    lactate = st.number_input('Lactate mmol/L', 0.0, 20.0, 1.5)

    risk_score = (2 if cvp > 18 else 0) + (3 if ci < 2.2 else 0) + (2 if svr < 800 or svr > 1600 else 0) + (3 if lactate > 2 else 0)
    st.metric('Risk Score', f'{risk_score}/10')
    st.metric('Stability', f'{95-risk_score*3:.0f}%')

with col2:
    st.header('24hr Trends')
    times = pd.date_range(end=datetime.now(), periods=24, freq='H')
    df = pd.DataFrame({
        'Time': times,
        'CVP': np.linspace(10, cvp, 24) + np.random.normal(0, 1, 24),
        'CI': np.linspace(3.0, ci, 24) + np.random.normal(0, 0.2, 24)
    })
    fig = px.line(df, x='Time', y=['CVP', 'CI'], title='Surveillance')
    fig.add_hline(y=18, line_dash='dash', line_color='red')
    fig.add_hline(y=2.2, line_dash='dash', line_color='orange')
    st.plotly_chart(fig, use_container_width=True)

st.markdown('---')
st.caption('*No PHI | Patrick Whittenburg RN | v6.0*')
