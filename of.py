import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import openai

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

# Initialize OpenAI client safely
@st.cache_resource
def get_openai_client():
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return None
        return openai.OpenAI(api_key=api_key)
    except Exception as e:
        st.warning(f"OpenAI setup failed: {e}")
        return None

client = get_openai_client()

# Sound helper
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
    
    if client is None:
        st.error("⚠️ OPENAI_API_KEY not configured. See setup instructions below.")
    
    # Display chat messages
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input with sound
    if prompt := st.chat_input("CVP high? ECMO weaning? Or anything else..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            play_click_sound()

        if client is not None:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                with st.spinner("AI thinking..."):
                    try:
                        for chunk in client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=st.session_state.messages,
                            stream=True
                        ):
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        play_click_sound()
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    except Exception as e:
                        st.error(f"OpenAI Error: {str(e)}")
        else:
            with st.chat_message("assistant"):
                st.error("❌ OpenAI API key not configured")

# Main dashboard
col1, col2 = st.columns(2)
with col1:
    st.header("📊 Live Vitals")
    cvp = st.number_input("CVP (mmHg)", 0.0, 50.0, 12.0, on_change=play_click_sound)
    ci = st.number_input("CI (L/min/m²)", 0.0, 10.0, 2.8, on_change=play_click_sound)
    svr = st.number_input("SVR (dynes)", 0, 3000, 1200, on_change=play_click_sound)
    lactate = st.number_input("Lactate (mmol/L)", 0.0, 20.0, 1.5, on_change=play_click_sound)

    risk_score = (2 if cvp >= 18 else 0) + (3 if ci <= 2.2 else 0) + (2 if svr <= 800 or svr >= 1600 else 0) + (3 if lactate >= 2 else 0)
    st.metric("Risk Score", f"{risk_score}/10", on_change=play_click_sound)
    st.metric("Stability", f"{95 - risk_score * 3:.0f}%", on_change=play_click_sound)

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

if st.button("Test Click Sound", on_click=play_click_sound):
    st.balloons()

# Setup Instructions
with st.expander("🔧 Setup Instructions - OpenAI API"):
    st.markdown("""
    ### How to Configure OpenAI API Key
    
    ✅ **Your API key has been configured on Streamlit Cloud!**
    
    Your app should now be working with the OpenAI AI chat feature.
    
    If you need to update the key in the future:
    
    1. **Go to Streamlit Cloud Settings:**
       - Visit https://share.streamlit.io
       - Click on your app
       - Click "Settings" (⚙️)
       - Go to "Secrets"
    
    2. **Update the API Key:**
       ```
       OPENAI_API_KEY = "your-new-key-here"
       ```
    
    3. **For Local Testing:**
       - Create `.streamlit/secrets.toml` in your project
       - Add: `OPENAI_API_KEY = "your-key-here"`
       - Run: `streamlit run of.py`
    
    ⚠️ **Important:** Never commit your API key to GitHub!
    """)
