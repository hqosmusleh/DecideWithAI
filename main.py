import os
import logging
from flask import Flask, render_template, request, flash
from openai import OpenAI
import openai

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-only-for-local-testing")
if app.config["SECRET_KEY"] == "dev-key-only-for-local-testing":
    logger.warning("Using default SECRET_KEY for development. Set SECRET_KEY environment variable for production.")

# OpenAI client
try:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    error_message = ""
    
    if request.method == "POST":
        try:
            # Get form data with validation
            decision = request.form.get("decision", "").strip()
            mood = request.form.get("mood", "Neutral").strip()
            
            # Validate input
            if not decision:
                error_message = "Please enter a decision you need help with."
                return render_template("index.html", error_message=error_message)
            
            if len(decision) > 500:
                error_message = "Please keep your decision under 500 characters."
                return render_template("index.html", error_message=error_message)
            
            # Check if OpenAI client is available
            if not client:
                error_message = "AI service is currently unavailable. Please try again later."
                return render_template("index.html", error_message=error_message)
            
            # Create optimized prompt based on mood
            mood_context = {
                "Happy": "The user is feeling positive and optimistic. Provide upbeat, encouraging suggestions.",
                "Neutral": "The user is feeling balanced and calm. Provide balanced, logical suggestions.",
                "Anxious": "The user is feeling worried or anxious. Provide reassuring, calming suggestions that reduce stress.",
                "Excited": "The user is feeling energetic and excited. Channel this energy into positive suggestions.",
                "Tired": "The user is feeling low energy or tired. Provide simple, easy-to-implement suggestions.",
                "Confused": "The user is feeling uncertain. Provide clear, structured suggestions that help clarify options."
            }
            
            system_prompt = f"""You are a wise and empathetic AI decision advisor. {mood_context.get(mood, mood_context['Neutral'])}

Guidelines:
- Provide 2-3 ranked suggestions
- Include brief reasoning for each suggestion
- Consider the user's emotional state
- Be practical and actionable
- Keep responses concise but helpful
- Use a warm, supportive tone"""

            user_prompt = f"I need help deciding: {decision}\n\nMy current mood: {mood}\n\nPlease provide your best suggestions with reasoning."

            # Make API call with error handling
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.7,
                timeout=30
            )
            
            ai_response = response.choices[0].message.content
            if ai_response:
                ai_response = ai_response.strip()
            
            # Validate response
            if not ai_response:
                error_message = "AI generated an empty response. Please try again."
                
        except openai.AuthenticationError:
            error_message = "AI service authentication failed. Please check configuration and try again."
            logger.error("OpenAI authentication failed")
            
        except openai.RateLimitError:
            error_message = "Too many requests. Please wait a moment and try again."
            logger.error("OpenAI rate limit exceeded")
            
        except openai.APITimeoutError:
            error_message = "AI service timed out. Please try again with a shorter question."
            logger.error("OpenAI timeout error")
            
        except openai.APIConnectionError:
            error_message = "Unable to connect to AI service. Please check your internet connection and try again."
            logger.error("OpenAI connection error")
            
        except openai.BadRequestError as e:
            error_message = "Invalid request. Please try rephrasing your question."
            logger.error(f"OpenAI bad request: {e}")
            
        except openai.NotFoundError:
            error_message = "AI model is currently unavailable. Please try again later."
            logger.error("OpenAI model not found")
            
        except Exception as e:
            error_message = "An unexpected error occurred. Please try again."
            logger.error(f"Unexpected error: {e}")

    return render_template("index.html", ai_response=ai_response, error_message=error_message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
@app.route("/healthz")
def healthz():
    return "OK", 200
