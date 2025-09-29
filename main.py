from flask import Flask, render_template, request
import os
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = None
    error_message = None

    if request.method == "POST":
        decision = request.form.get("decision")
        mood = request.form.get("mood")
        
        if not decision:
            error_message = "Please enter a decision you need help with."
        else:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful decision-making assistant."},
                        {"role": "user", "content": f"User decision: {decision}\nMood: {mood}"}
                    ],
                    max_tokens=150,
                )
                ai_response = response.choices[0].message.content.strip()
            except Exception as e:
                error_message = str(e)

    return render_template("index.html", ai_response=ai_response, error_message=error_message)

@app.route("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
