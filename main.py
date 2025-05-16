import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a supported model (fast & reliable)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def generate_quote_post():
    prompt = (
        "Give me one original motivational quote, a short Instagram caption for it, "
        "and 10 trending related hashtags."
    )
    response = model.generate_content(prompt)
    print("🌟 Generated Instagram Post:\n")
    print(response.text)

if __name__ == "__main__":
    generate_quote_post()
