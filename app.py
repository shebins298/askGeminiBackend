from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
import traceback

app = Flask(__name__)
CORS(app, origins="*")  # Allow all origins (or specify only GitHub Pages URL)

# Gemini API setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2")  # Ensure the model is correctly named for 2.0

@app.route("/", methods=["GET"])
def home():
    return "✅ Gemini backend is live!", 200

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        print(f"Received prompt: {prompt}")
        # TEMP: Just return dummy data to verify front-end works
        return jsonify({"response": f"You said: {prompt}"})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        # Log the full traceback for detailed error info
        print(f"Error: {str(e)}")
        print("Stack trace:", traceback.format_exc())  # This will show the full error stack trace
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
