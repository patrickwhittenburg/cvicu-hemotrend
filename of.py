import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import openai  # New: For full AI

# MUST be first Streamlit command
st.set_page_config(layout="wide")

# Custom CSS with sound-ready elements
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600&display=swap');
    .stApp { background: linear-gradient(135deg, #0a0a0f 0%, #1e1e2f 100%); }
    h1 { color: #00d4aa !important; font-size: 3rem !important; font-weight: 600 !important; }
    .stMetric label { color: rgba(255,255,255,0.9) !important; }
    .ai-response { background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 16px; border-left: 4px solid #00d4aa; }
    </style>
""", unsafe_allowhtml=True)

st.title("🤖 HemoTrend Pro v7 - Full AI CVICU Assistant")

# Initialize OpenAI client (add to .streamlit/secrets.toml: OPENAI_API_KEY = "sk-...")
@st.cache_resource
def get_openai_client():
    return openai.OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

client = get_openai_client()

# Sound helper (add 'click.mp3' to your app folder - free from freesound.org)
def play_click_sound():
    click_html = """
    <audio id="clickSound" preload="auto">
        <source src="click.mp3" type="audio/mpeg">
    </audio>
    <script>
        document.getElementById('clickSound').play();
    </script>
    """
    st.markdown(click_html, unsafe_allowhtml=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are CVICU Pro AI by Patrick Whittenburg RN. Expert in cardiac ICU: ECMO, Swan-Ganz, drips, MAZE, hemodynamics. Answer ANY question accurately, prioritize clinical judgment."}
    ]

# Sidebar: Enhanced AI Chat
with st.sidebar:
    st.header("🧠 AI Chat - Ask Anything")
    # Display chat messages
    for message in st.session_state.messages[1:]:  # Skip system
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input with sound
    if prompt := st.chat_input("CVP high? ECMO weaning? Or anything else..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            play_click_sound()  # Sound on send

        # Generate AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("AI thinking..."):
                for chunk in client.chat.completions.create(
                    model="gpt-4o-mini",  # Or gpt-3.5-turbo
                    messages=st.session_state.messages,
                    stream=True
                ):
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            play_click_sound()  # Sound on response
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Main dashboard - preserved + sounds
col1, col2 = st.columns(2)
with col1:
    st.header("📊 Live Vitals")
    cvp = st.number_input("CVP (mmHg)", 0.0, 50.0, 12.0, on_change=play_click_sound)
    ci = st.number_input("CI (L/min/m²)", 0.0, 10.0, 2.8, on_change=play_click_sound)
    svr = st.number_input("SVR (dynes)", 0, 3000, 1200, on_change=play_click_sound)
    lactate = st.number_input("Lactate (mmol/L)", 0.0, 20.0, 1.5, on_change=play_click_sound)

    risk_score = (2 if cvp >= 18 else 0) + (3 if ci <= 2.2 else 0) + (2 if svr <= 800 or svr >= 1600 else 0) + (3 if lactate >= 2 else 0)
    st.metric("Risk Score", f"{risk_score}/10", on_change=play_click_sound)
    st.metric("Stability", f"{95 - risk_score * 3:.0f}%,", on_change=play_click_sound)

with col2:
    st.header("📈 24hr Trends")
    times = pd.date_range(end=datetime.now(), periods=24, freq='H')
    df = pd.DataFrame({
        'Time': times,
        'CVP': np.linspace(10, cvp, 24) + np.random.normal(0, 1, 24),
        'CI': np.linspace(3.0, ci, 24) + np.random.normal(0, 0.2, 24)
    })
    fig = px.line(df, x='Time', y=['CVP', 'CI'], title="Surveillance")
    fig.add_hline(y=18, line_dash="dash", line_color="red")
    fig.add_hline(y=2.2, line_dash="dash", line_color="orange")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("No PHI. Patrick Whittenburg RN v7.0 - Full AI + Sounds 🚀")

# Experimental: Global click sound button for testing
if st.button("Test Click Sound", on_click=play_click_sound):
    st.balloons()