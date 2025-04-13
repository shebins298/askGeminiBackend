from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)

# Enable CORS for all origins (can replace "*" with specific origins like your GitHub Pages URL)
CORS(app, origins="*")

# Configure Gemini API using your API key from environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")  # Specify the Gemini 1.5 Flash model

@app.route("/", methods=["GET"])
def home():
    return "✅ Gemini 1.5 Flash backend is live!", 200

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        # Handle CORS preflight request
        return '', 200

    # Handle POST request to generate content
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Use Gemini 1.5 Flash to generate content
        response = model.generate(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
