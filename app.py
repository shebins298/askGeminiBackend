from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app, origins="*")  # Allow all origins (or specify only GitHub Pages URL)

# Gemini 2 API setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2")  # Specify Gemini 2 model name

@app.route("/", methods=["GET"])
def home():
    return "✅ Gemini 2 backend is live!", 200

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        # Preflight request — just return ok
        return '', 200

    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Log the prompt to ensure it's correctly received
        print(f"Received prompt: {prompt}")

        # Use the appropriate API method for text generation (based on available methods)
        response = model.complete(prompt)  # Adjusted method to 'complete', as 'generate' might not exist in Gemini 2

        # Log the response to see what we get from the API
        print(f"Response from Gemini API: {response}")

        return jsonify({"response": response.text})
    
    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
