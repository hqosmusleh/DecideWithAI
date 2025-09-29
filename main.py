# main.py
from flask import Flask, render_template, request
import openai
import os

# -----------------------------
# Configuration
# -----------------------------
app = Flask(__name__)

# Make sure your OpenAI API key is set as an environment variable
# For example, in Render: Environment -> Add OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = None
    error_message = None

    if request.method == "POST":
        decision = request.form.get("decision", "").strip()
        mood = request.form.get("mood", "").strip()

        if not decision:
            error_message = "Please enter a decision to proceed."
        else:
            try:
                # Call OpenAI API (Chat Completions)
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant giving advice for decisions based on the user's mood."
                        },
                        {
                            "role": "user",
                            "content": f"I need help with this decision: '{decision}'. My mood is '{mood}'."
                        }
                    ],
                    temperature=0.7,
                    max_tokens=250
                )
                ai_response = response.choices[0].message.content.strip()

            except openai.error.AuthenticationError:
                error_message = "Authentication failed. Please check your OpenAI API key."
            except openai.error.OpenAIError as e:
                error_message = f"OpenAI API error: {str(e)}"
            except Exception as e:
                error_message = f"An unexpected error occurred: {str(e)}"

    return render_template("index.html", ai_response=ai_response, error_message=error_message)


# -----------------------------
# Run the App
# -----------------------------
if __name__ == "__main__":
    # Set host="0.0.0.0" for Render or other cloud services
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
