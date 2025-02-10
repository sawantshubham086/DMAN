from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import random
import time
import os

app = Flask(__name__)

# Configure Google PaLM API
API_KEY = 'AIzaSyDtThly7bxHnLybhqsmfTZaVG6zhH-zRcQ'  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Configure the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

class DeadmanBot:
    def __init__(self):
        self.name = "DEADMAN"
        self.greetings = [
            "Hey there! How's it going? 😊",
            "Hi! Nice to meet you! 👋",
            "Hello! I'm DEADMAN, how can I help you today? 💫",
            "Hey! I'm here to chat with you! 🌟"
        ]
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Start a new conversation
        self.chat = self.model.start_chat(history=[])

    def get_ai_response(self, user_input):
        try:
            # Generate response using the chat
            response = self.chat.send_message(
                user_input,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Add emojis to make response more friendly
            response_text = response.text + " 😊"
            return response_text
            
        except Exception as e:
            print(f"API Error: {str(e)}")  # For debugging
            return f"I apologize, but I encountered an error. Could you rephrase your question? 🤔 Error: {str(e)}"

    def respond(self, user_input):
        user_input = user_input.lower().strip()
        
        # Check for basic interactions first
        if any(word in user_input for word in ["hi", "hello", "hey", "greetings"]):
            return random.choice(self.greetings)
        
        # For all other queries, use Google's AI
        response = self.get_ai_response(user_input)
        return response

bot = DeadmanBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    
    # Add a small delay to simulate thinking
    time.sleep(0.5)
    
    response = bot.respond(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 