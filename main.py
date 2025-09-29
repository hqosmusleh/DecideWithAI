import os
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "mydefaultsecret")

# OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    if request.method == "POST":
        decision = request.form.get("decision", "")
        mood = request.form.get("mood", "")
        prompt = f"Help me make a decision. Decision: {decision}. Mood: {mood}. Give me ranked suggestions with short reasoning."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_response = response.choices[0].message.content

    return render_template("index.html", ai_response=ai_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
