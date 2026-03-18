from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

# Initialize OpenAI client
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("Missing OPENAI_API_KEY in secrets. Please configure it in .streamlit/secrets.toml")
    st.stop()

# Initialize session state with consistent dot notation
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=st.session_state.openai_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error communicating with OpenAI: {str(e)}")
            # Remove the user message if API call failed
            st.session_state.messages.pop()