from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime
import uuid

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client["gla_chatbot"]
chat_sessions = db["chat_sessions"]
chat_messages = db["chat_messages"]

def create_session(title="New Chat"):
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    session = {
        "session_id": session_id,
        "title": title,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    }
    chat_sessions.insert_one(session)
    return session_id

def get_all_sessions():
    """Get all chat sessions ordered by most recent first"""
    return list(chat_sessions.find().sort("updated_at", -1))

def get_session(session_id):
    """Get a specific chat session by ID"""
    return chat_sessions.find_one({"session_id": session_id})

def update_session_title(session_id, title):
    """Update a chat session's title"""
    chat_sessions.update_one(
        {"session_id": session_id},
        {"$set": {
            "title": title,
            "updated_at": datetime.datetime.now()
        }}
    )

def save_chat_message(user_message, bot_response, session_id=None):
    """Save chat message to MongoDB within a session"""
    # Skip saving if user message is empty
    if not user_message or not user_message.strip():
        return session_id
    
    # If no session_id provided, create a new session
    if not session_id:
        session_id = create_session(title=user_message[:30] + "..." if len(user_message) > 30 else user_message)
    
    # Update the session's last updated time
    chat_sessions.update_one(
        {"session_id": session_id},
        {"$set": {"updated_at": datetime.datetime.now()}}
    )
    
    # Save the message
    chat_messages.insert_one({
        "session_id": session_id,
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.datetime.now()
    })
    
    return session_id

def get_chat_history_for_session(session_id):
    """Retrieve all messages for a specific chat session"""
    return list(chat_messages.find({"session_id": session_id}).sort("timestamp", 1))

def get_chat_history(limit=10):
    """Retrieve recent chat history across all sessions"""
    return list(chat_messages.find().sort("timestamp", -1).limit(limit)) 