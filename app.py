import google.generativeai as genai
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Sameer AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Custom CSS (Chote, Clean Text aur Compact Layout ke liye)
st.markdown(
    """
    <style>
    /* Streamlit Headers & Menus Hide */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global Compact Font Styling */
    html, body, [class*="css"] {
        font-size: 14px !important;
    }

    /* About Section Styling (Left-aligned & Small Text) */
    .about-card {
        background-color: #f8f9fa;
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 4px solid #1a73e8;
        margin-top: 15px;
        margin-bottom: 20px;
        text-align: left;
    }
    .about-card h4 {
        margin-top: 0;
        margin-bottom: 8px;
        font-size: 16px;
        color: #202124;
    }
    .about-card p {
        margin: 4px 0;
        font-size: 13.5px;
        color: #4a4a4a;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Header & Welcome Message
st.title("🤖 Welcome to Sameer AI")
st.caption("Developed by Sameer | Powered by Advanced AI")

# 4. Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. About Section (Sirf Chat Start hone se pehle dikhega)
if len(st.session_state.messages) == 0:
    st.markdown(
        """
        <div class="about-card">
            <h4>📌 About the Creator</h4>
            <p><b>Name:</b> Mohammad Sameer</p>
            <p><b>Field:</b> Electrical Engineering</p>
            <p style="margin-top: 8px;">Welcome to Sameer AI! Ask any questions or solve problems easily.</p>
            <hr style="margin: 10px 0; border: 0; border-top: 1px solid #ddd;">
            <p style="font-size: 12px; color: #777;">Created with ❤️ by Sameer</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    with st.sidebar:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

# 6. API Key Verification
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error(
        "API Key missing! Please configure GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()

# 7. Configure Model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 8. Display Chat Messages Below Title
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. Handle User Input
if prompt := st.chat_input("Ask something..."):
    # User message add karein
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Page rerun taaki About Section turant gayab ho jaye
    st.rerun()

# 10. Generate Response
if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
):
    with st.chat_message("assistant"):
        try:
            user_prompt = st.session_state.messages[-1]["content"]
            response = model.generate_content(user_prompt)
            st.markdown(response.text)
            st.session_state.messages.append(
                {"role": "assistant", "content": response.text}
            )
            st.rerun()
        except Exception as e:
            st.error(f"Error generating response: {e}")
