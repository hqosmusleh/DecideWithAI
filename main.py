# main.pyfrom flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ai", methods=["POST"])
def ai():
    user_decision = request.form.get("decision")

    if not user_decision:
        return render_template("index.html", ai_result="⚠️ Please enter a decision to proceed.")

    # Example AI logic (replace with your own later)
    ai_output = f"🤖 AI suggests: Based on '{user_decision}', the smarter choice would be option A."

    return render_template("index.html", ai_result=ai_output)

if __name__ == "__main__":
    app.run(debug=True)

# -----------------------------
# Run the App
# -----------------------------
if __name__ == "__main__":
    # Set host="0.0.0.0" for Render or other cloud services
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
