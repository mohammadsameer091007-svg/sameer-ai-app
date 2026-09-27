import google.generativeai as genai
import streamlit as st
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_dict=True,
)
# Page Configuration
st.set_page_config(page_title="Sameer AI", page_icon="🤖")

# Custom Title & Developer Details
st.title("🤖 Welcome to Sameer AI")
st.caption("Developed by Sameer | Powered by Advanced AI")

# Sidebar - Creator Information
with st.sidebar:
    st.header("About the Creator")
    st.write("**Name:** Sameer")
    st.write(
        "Welcome to Sameer AI! This assistant is designed to help you answer questions, solve problems, and provide helpful insights."
    )
    st.markdown("---")
    st.write("Created with ❤️ by Sameer")

# Get API Key securely from secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error(
        "API Key missing! Please configure GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()

# Configure Gemini Model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.8-flash")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Sameer AI anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
    except Exception as e:
        st.error(f"Error generating response: {e}")
