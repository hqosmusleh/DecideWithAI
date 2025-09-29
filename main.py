from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/generate", methods=["POST"])
def generate():
    decision = request.form.get("decision")
    if not decision:
        return jsonify({"error": "Please enter a decision to proceed."})

    # Call OpenAI's chat completion API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Help me decide: {decision}"}]
    )
    result = response.choices[0].message.content
    return jsonify({"response": result})

@app.route("/")
def index():
    # Serves your index.html file
    return app.send_static_file("index.html")
