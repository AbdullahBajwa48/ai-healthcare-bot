import streamlit as st
from bot import get_response

st.set_page_config(page_title="Healthcare Information Bot", page_icon="💬")
st.title("💬 Healthcare Information Bot")
st.write("Welcome to the Healthcare Information Bot! Ask me anything about health and wellness.")

st.sidebar.title("Disclaimer")
st.sidebar.info("""
This bot provides general health information and wellness guidance only. 
It does NOT diagnose medical conditions or recommend specific treatments. 
For any serious symptoms, please call emergency services immediately. 
Always consult a qualified doctor for personal medical advice.
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Static greeting
st.chat_message("assistant").markdown(
    "Hello! I'm here to provide general health information and wellness guidance. Ask me anything!"
)

# Render conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input + response
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = st.write_stream(get_response(st.session_state.messages))

    st.session_state.messages.append({"role": "assistant", "content": response})