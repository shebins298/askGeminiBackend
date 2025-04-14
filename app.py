from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app, origins=["https://shebins298.github.io"])

# Configure Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")  # You can change to "gemini-2" if available

@app.route("/", methods=["GET"])
def home():
    return "✅ Gemini backend is live!", 200

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return '', 200  # Preflight CORS check

    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        print(f"📥 Prompt received: {prompt}")
        chat = model.start_chat()
        response = chat.send_message(prompt)
        print(f"📤 Gemini Response: {response.text}")
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
