import google.generativeai as genai
import streamlit as st

# Page Config
st.set_page_config(page_title="Sameer AI", page_icon="🤖")

# --- Header Section (Your Info) ---
st.title("🤖 Sameer AI Assistant")
st.write("👋 **नमस्ते! मैं समीर का AI असिस्टेंट हूँ।**")
st.write("📍 **Location:** Naraina, Jaipur Rural, Rajasthan")
st.write("🎓 **Qualification:** Diploma in Electrical Engineering")
st.write("---")

# --- Gemini AI Chat Section ---
st.subheader("💬 Ask Me Anything")

api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
  api_key = st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel("gemini-1.5-flash")

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      response = model.generate_content(prompt)
      st.markdown(response.text)
      st.session_state.messages.append(
          {"role": "assistant", "content": response.text}
      )
