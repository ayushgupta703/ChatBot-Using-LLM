from flask import Flask, render_template, request, jsonify
from main import get_chatbot_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    bot_response = get_chatbot_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
