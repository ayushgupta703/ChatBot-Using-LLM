from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client["gla_chatbot"]
chat_history = db["chat_history"]

def save_chat_message(user_message, bot_response):
    """Save chat message to MongoDB"""
    chat_history.insert_one({
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.datetime.now()
    })

def get_chat_history(limit=10):
    """Retrieve recent chat history"""
    return list(chat_history.find().sort("timestamp", -1).limit(limit)) 