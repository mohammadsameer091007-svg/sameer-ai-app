import google.generativeai as genai
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Sameer AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Clean Styling
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

# 3. Header & Welcome Message Always Fixed at Top
st.title("🤖 Welcome to Sameer AI")
st.caption("Developed by Sameer | Powered by Advanced AI")

# 4. Initialize Session State
if "messages" not in st.session_state:
  st.session_state.messages = []

# 5. About Section (Sirf Chat Start hone se Pahle Dikhega)
if len(st.session_state.messages) == 0:
  st.markdown("---")
  st.markdown("### 📌 About the Creator")
  st.write("**Name:** Mohammad Sameer")
  st.write("**Field:** Electrical Engineering")
  st.write(
      "Welcome to Sameer AI! Ask any questions or solve problems easily."
  )
  st.markdown("---")
  st.write("Created with ❤️ by Sameer")
  st.markdown("---")
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

# 7. Configure Correct Model Name
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.5-flash")

# 8. Display Chat Messages Below Title
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# 9. Handle User Input
if prompt := st.chat_input("Ask something..."):
  # User ka message add karein
  st.session_state.messages.append({"role": "user", "content": prompt})

  # Instant UI update ke liye rerun karein (jisse 'About Section' turant gayab ho jaye)
  st.rerun()

# 10. Generate Response if last message is from user
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
