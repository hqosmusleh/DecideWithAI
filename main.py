# main.py
from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key here or via environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Recommended
# openai.api_key = "YOUR_API_KEY"  # Or hardcode directly (not recommended)

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = None
    error_message = None

    if request.method == "POST":
        decision = request.form.get("decision", "").strip()
        mood = request.form.get("mood", "").strip()

        if not decision:
            error_message = "Please enter a decision for the AI to consider."
        else:
            try:
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that gives advice based on a user's mood and decision."
                        },
                        {
                            "role": "user",
                            "content": f"Decision: {decision}\nMood: {mood}"
                        }
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                ai_response = r_
n.get("PORT", 10000)))
