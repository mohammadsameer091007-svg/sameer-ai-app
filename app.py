import os
from google import genai
import streamlit as st

# Page Config
st.set_page_config(page_title="Sameer AI", page_icon="🤖")

st.title("🤖 Welcome to Sameer AI")
st.caption("Created by Sameer | Powered by Gemini")

with st.sidebar:
    st.header("About Creator")
    st.write("**Developer:** Sameer")
    st.write("Welcome to Sameer AI! Ask me anything.")

# Get API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error(
        "API Key missing! Streamlit Secrets me GEMINI_API_KEY add karein."
    )
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Sameer AI..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
    except Exception as e:
        st.error(f"Error: {e}")
