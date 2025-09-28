from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Add your OpenAI API key here
openai.api_key = "YOUR_API_KEY"

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = None
    if request.method == "POST":
        decision = request.form["decision"]
        mood = request.form["mood"]

        prompt = f"Help me make a decision. Decision: {decision}. Mood: {mood}. Give me ranked suggestions with short reasoning."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly AI that helps people make everyday decisions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        ai_response = response["choices"][0]["message"]["content"]

    return render_template("index.html", ai_response=ai_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
