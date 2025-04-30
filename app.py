import streamlit as st
from main import get_chatbot_response
from db_config import (
    save_chat_message, 
    get_chat_history, 
    get_all_sessions,
    get_session,
    create_session,
    get_chat_history_for_session,
    update_session_title
)
import time
from datetime import datetime
import html

# Page config
st.set_page_config(
    page_title="GLA Chatbot", 
    page_icon="🤖", 
    layout="wide",  
    initial_sidebar_state="expanded"
)

# Custom styling with a more modern look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Add background gradient to the main content */
    .main {
        background: linear-gradient(135deg, #121212, #1e1e1e);
    }
    
    .chat-header {
        margin-bottom: 20px;
        background: linear-gradient(90deg, #4568DC, #B06AB3);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .chat-header h1 {
        margin: 0;
        color: white;
        font-weight: 600;
    }
    
    .chat-header p {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 0;
    }
    
    .chat-message {
        display: flex;
        margin-bottom: 16px;
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 12px;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #0078FF, #00C6FF);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    .bot-avatar {
        background: linear-gradient(135deg, #B06AB3, #4568DC);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    .message-content {
        flex: 1;
        padding: 12px 16px;
        border-radius: 12px;
        max-width: 80%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #0078FF, #00C6FF);
        color: white;
        border-top-right-radius: 0;
        align-self: flex-end;
        margin-left: auto;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .bot-message {
        background: #2E2E2E;
        color: white;
        border-top-left-radius: 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .input-area {
        display: flex;
        margin-top: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTextInput > div > div > input {
        color: white;
        background-color: transparent !important;
        border: none !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4568DC, #B06AB3);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3A57C5, #9B5BA0);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar styling */
    .sidebar-header {
        padding: 20px;
        text-align: center;
        color: white;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a1a, #2E2E2E);
    }
    
    .new-chat-btn {
        margin: 0 0 20px 0;
    }
    
    .new-chat-btn > div > button {
        background: linear-gradient(135deg, #4568DC, #B06AB3);
        border: none;
        color: white;
        font-weight: 500;
        text-align: center;
    }
    
    .new-chat-btn > div > button:hover {
        background: linear-gradient(135deg, #3A57C5, #9B5BA0);
        transform: translateY(-2px);
    }
    
    .chat-session {
        background: rgba(255, 255, 255, 0.05);
        margin-bottom: 8px;
        border-radius: 8px;
        overflow: hidden;
        transition: all 0.2s ease;
    }
    
    .chat-session:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .chat-session.active {
        background: rgba(69, 104, 220, 0.2);
        border-left: 3px solid #4568DC;
    }
    
    .chat-session > div > button {
        text-align: left;
        background: transparent;
        color: white;
        padding: 12px;
        border-radius: 0;
        font-weight: normal;
        display: block;
        width: 100%;
    }
    
    .chat-date {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 4px;
    }
    
    /* Loading spinner */
    .thinking {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    
    .dots {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px 16px;
        border-radius: 12px;
    }
    
    .dot {
        width: 8px;
        height: 8px;
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        margin: 0 4px;
        animation: pulse 1.5s infinite ease-in-out;
    }
    
    .dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes pulse {
        0% { transform: scale(0.8); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.8); opacity: 0.5; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "sessions" not in st.session_state:
    st.session_state.sessions = get_all_sessions()

if "thinking" not in st.session_state:
    st.session_state.thinking = False

# Function to switch to a session
def switch_to_session(session_id):
    st.session_state.current_session_id = session_id
    # Load messages for this session
    messages = get_chat_history_for_session(session_id)
    
    # Clear existing messages and load new ones
    st.session_state.messages = []
    for msg in messages:
        st.session_state.messages.append({"role": "user", "content": html.escape(msg["user_message"])})
        st.session_state.messages.append({"role": "bot", "content": html.escape(msg["bot_response"])})

# Function to format date for display
def format_date(dt):
    today = datetime.now().date()
    dt_date = dt.date()
    
    if dt_date == today:
        return f"Today, {dt.strftime('%I:%M %p')}"
    elif (today - dt_date).days == 1:
        return f"Yesterday, {dt.strftime('%I:%M %p')}"
    else:
        return dt.strftime("%b %d, %Y")

# Function to render messages with avatars
def render_message(role, content):
    if role == "user":
        avatar = """<div class="message-avatar user-avatar">👤</div>"""
        message_class = "user-message"
    else:
        avatar = """<div class="message-avatar bot-avatar">🤖</div>"""
        message_class = "bot-message"
        
    # Convert newlines to <br> tags for proper display
    formatted_content = content.replace('\n', '<br>')
        
    return f"""
    <div class="chat-message">
        {avatar}
        <div class="message-content {message_class}">
            {formatted_content}
        </div>
    </div>
    """

# Function to handle message sending
def handle_send():
    user_input = st.session_state.user_input
    if user_input.strip():  # Only process non-empty inputs
        # Add message to display with HTML escaping
        st.session_state.messages.append({"role": "user", "content": html.escape(user_input)})
        
        # Show thinking animation
        st.session_state.thinking = True
        st.rerun()
    else:
        # Clear the input field if it's empty
        st.session_state.user_input = ""

# Sidebar - Chat History
with st.sidebar:
    st.markdown("<div class='sidebar-header'><h1>💬 Chat History</h1></div>", unsafe_allow_html=True)
    
    # New Chat button
    with st.container():
        st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
        if st.button("✨ New Chat", use_container_width=True):
            # Clear the messages but don't create a session yet
            # Session will be created only when the user sends the first message
            st.session_state.current_session_id = None
            st.session_state.messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Session list
    st.markdown("### Recent Conversations")
    
    if not st.session_state.sessions:
        st.markdown("<p style='color: rgba(255,255,255,0.5); text-align: center; padding: 20px;'>No conversations yet</p>", unsafe_allow_html=True)
    
    for session in st.session_state.sessions:
        session_id = session["session_id"]
        title = session["title"]
        
        # Format date for display
        date_str = format_date(session["created_at"])
        
        # Active class for current session
        active_class = "active" if st.session_state.current_session_id == session_id else ""
        
        # Use a unique key for each button
        btn_key = f"session_{session_id}"
        
        # Create a container with the right class
        st.markdown(f"<div class='chat-session {active_class}'>", unsafe_allow_html=True)
        
        # Display the session button with just the title
        if st.button(f"{title}", key=btn_key, use_container_width=True):
            switch_to_session(session_id)
            st.rerun()
        
        # Display the date separately after the button
        st.markdown(f"<div class='chat-date' style='padding-left: 12px; margin-top: -15px;'>{date_str}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Main content area - chat interface
# Header
st.markdown("""
    <div class='chat-header'>
        <h1>🤖 GLA Chatbot</h1>
        <p>Ask me anything about the Global Learning Academy!</p>
    </div>
""", unsafe_allow_html=True)

# Chat display area
chat_container = st.container()

with chat_container:
    
    # Display chat messages or welcome message if empty
    if st.session_state.messages:
        for msg in st.session_state.messages:
            st.markdown(
                render_message(msg["role"], msg["content"]), 
                unsafe_allow_html=True
            )
    else:
        st.markdown("""
            <div style="text-align: center; padding: 40px 20px; color: rgba(255,255,255,0.7);">
                <p>Type a message to start chatting with the GLA Assistant</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Display thinking animation if needed
    if st.session_state.thinking:
        st.markdown("""
            <div class="thinking">
                <div class="dots">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Second-phase function that gets called after thinking animation is shown
if st.session_state.thinking:
    user_input = st.session_state.user_input
    st.session_state.user_input = ""  # Clear input field
    
    # Get bot response
    response = get_chatbot_response(user_input)
    
    # Process response to escape any HTML tags if needed
    processed_response = html.escape(response)
    
    # Add response to display
    st.session_state.messages.append({"role": "bot", "content": processed_response})
    
    # If no current session, create one when first message is sent
    if not st.session_state.current_session_id and user_input.strip():
        st.session_state.current_session_id = save_chat_message(user_input, response)
        # The save_chat_message function already sets the title based on the first message
    elif st.session_state.current_session_id and user_input.strip():
        # If this is the first message in an existing session, update the title
        if len(st.session_state.messages) == 2:  # First user message and bot response
            # Create a title from the first message
            title = user_input[:30] + "..." if len(user_input) > 30 else user_input
            update_session_title(st.session_state.current_session_id, title)
        
        # Save to existing session
        save_chat_message(user_input, response, st.session_state.current_session_id)
    
    # Refresh sessions list
    st.session_state.sessions = get_all_sessions()
    
    # Stop thinking animation
    st.session_state.thinking = False
    # Add a rerun here to ensure the UI updates immediately after response
    st.rerun()

# Input area
st.markdown("<div class='input-area'>", unsafe_allow_html=True)
input_cols = st.columns([6, 1])

with input_cols[0]:
    st.text_input(
        "User message",
        key="user_input",
        placeholder="Type your message here...",
        label_visibility="collapsed",
        on_change=handle_send
    )

with input_cols[1]:
    if st.button("Send", use_container_width=True):
        handle_send()
        
st.markdown("</div>", unsafe_allow_html=True)
    
