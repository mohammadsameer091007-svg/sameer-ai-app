import google.generativeai as genai
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Sameer AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",  # Sidebar ko by default hidden rakha hai
)

# 2. Top Header & Footer Hide Karne Ke Liye Clean Styling
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Main Title
st.title("🤖 Welcome to Sameer AI")
st.caption("Developed by Sameer | Powered by Advanced AI")

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Creator Info Card (Keval CHAT START HONE SE PEHLE dikhega)
if len(st.session_state.messages) == 0:
    st.markdown("---")
    st.markdown("### 📌 About the Creator")
    st.write("**Name:** Mohammad Sameer")
    st.write("**Field:** Electrical Engineering")
    st.write(
        "Welcome to Sameer AI! This assistant is designed to help you answer"
        " questions, solve problems, and provide helpful insights."
    )
    st.markdown("---")
    st.write("Created with ❤️ by Sameer")
    st.markdown("---")

# 6. Clear Chat History Button (Chat shuru hone ke baad niche dikhega)
else:
    with st.sidebar:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

# 7. Get API Key securely from secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error(
        "API Key missing! Please configure GEMINI_API_KEY in Streamlit"
        " Secrets."
    )
    st.stop()

# 8. Configure Gemini Model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")
# 9. Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 10. User Input & AI Response
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
        st.rerun()  # Screen refresh karke Creator Card ko hata dega
    except Exception as e:
        st.error(f"Error generating response: {e}")
