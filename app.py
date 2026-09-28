import google.generativeai as genai
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Sameer AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 2. Streamlit Footer, GitHub Icon aur Edit Option Hide Karne Ke Liye
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* GitHub Icon aur Edit Button Chhipane Ke Liye */
    .stAppHeader a[aria-label*="GitHub"],
    .stAppHeader button[title*="Edit"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Title Display
st.title("🤖 Welcome to Sameer AI")
st.caption("Developed by Sameer | Powered by Advanced AI")

# 4. Sidebar - Creator Information & Clear Chat Button
with st.sidebar:
    st.header("About the Creator")
    st.write("**Name:** Sameer")
    st.write(
        "Welcome to Sameer AI! This assistant is designed to help you answer"
        " questions, solve problems, and provide helpful insights."
    )
    st.markdown("---")
    st.write("Created with ❤️ by Sameer")
    st.markdown("---")

    # Clear Chat History Button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 5. Get API Key securely from secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error(
        "API Key missing! Please configure GEMINI_API_KEY in Streamlit"
        " Secrets."
    )
    st.stop()

# 6. Configure Gemini Model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 7. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 8. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. User Input & AI Response
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
