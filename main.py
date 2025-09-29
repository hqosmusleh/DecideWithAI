# main.py
from flask import Flask, render_template, request
import os
import openai

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    decision = None
    error_msg = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if not user_input:
            error_msg = "Please enter a decision you need help with."
        else:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful decision-making assistant."},
                        {"role": "user", "content": user_input},
                    ],
                    max_tokens=150,
                )
                decision = response.choices[0].message.content.strip()
            except Exception as e:
                error_msg = f"Error: {str(e)}"
    return render_template("index.html", decision=decision, error_msg=error_msg)

@app.route("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
