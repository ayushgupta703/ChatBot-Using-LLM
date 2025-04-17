import streamlit as st
from main import get_chatbot_response

# Page config
st.set_page_config(page_title="GLA Chatbot", page_icon="🤖", layout="centered")

# Custom styles
st.markdown("""
    <style>
    .chat-box {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 20px;
        height: 400px;
        overflow-y: auto;
    }
    .user-msg {
        text-align: right;
        background: #0078FF;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: white;
    }
    .bot-msg {
        text-align: left;
        background: #444;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 GLA Chatbot")
st.markdown("Ask me anything about the Global Learning Academy!")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle message sending
def handle_send():
    user_input = st.session_state.user_input
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = get_chatbot_response(user_input)
        st.session_state.messages.append({"role": "bot", "content": response})
        st.session_state.user_input = ""  # Clears input box

# Display chat messages
with st.container():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

# Input field
st.text_input("Type your message here...", key="user_input", on_change=handle_send)
