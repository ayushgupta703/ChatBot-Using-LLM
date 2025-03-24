import json
import google.generativeai as genai

# Configure Gemini
API_KEY = "AIzaSyD3hwKdDESvUyjHhWoa-MbgEAMbXCy7_uQ"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Initialize the model correctly
model = genai.GenerativeModel('gemini-1.5-flash-latest')  # Use exact model name

# Load the JSON data
with open('chatbot_data.json', 'r') as f:
    knowledge_base = json.load(f)


def create_context(knowledge_base):
    """Convert JSON data into a context string"""
    context = "You are a helpful assistant for The Global Learning Academy. Here is the information:\n\n"
    for item in knowledge_base:
        context += f"Question: {item['question']}\nAnswer: {item['answer']}\n"
        if 'details' in item:
            context += f"Details:\n- Description: {item['details']['description']}\n"
            context += f"- Topics: {', '.join(item['details']['topics_covered'])}\n"
            context += f"- Outcomes: {', '.join(item['details']['learning_outcomes'])}\n"
        context += "\n"
    return context


def generate_response(user_input):
    """Generate response using Gemini with context"""
    prompt = f"""
    Context:
    {create_context(knowledge_base)}

    Instructions:
    1. Answer using only the provided context
    2. Be concise and accurate
    3. If unsure, say you don't know

    Question: {user_input}
    Answer:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"I couldn't find that information. (Error: {str(e)})"


# Chatbot interface
print("Welcome to Global Learning Academy Chatbot!")
print("Ask about courses or faculty. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Chatbot: Thank you for chatting!")
        break

    response = generate_response(user_input)
    print(f"Chatbot: {response}\n")