from flask import Flask, render_template, request, jsonify
import os
import openai

# Set global API key for OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        user_input = request.form.get("decision", "").strip()

        if not user_input:
            return jsonify({"error": "Please enter a decision to proceed."}), 400

        # Call OpenAI ChatCompletion API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful decision-making assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100
        )

        ai_reply = response.choices[0].message.content.strip()
        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
