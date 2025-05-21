import os
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import google.generativeai as genai
from dotenv import load_dotenv
import random
from instabot import Bot



# Load API keys
load_dotenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# 1. Download a blurred background from Unsplash
def get_blurred_background(topic="motivation", output_path="background.jpg"):
    url = f"https://api.unsplash.com/photos/random?query={topic}&orientation=squarish&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    image_url = response.json()['urls']['full']
    img_data = requests.get(image_url).content

    with open(output_path, 'wb') as handler:
        handler.write(img_data)

    # Apply blur
    img = Image.open(output_path).resize((1080, 1080)).filter(ImageFilter.GaussianBlur(12))
    img.save(output_path)
    return output_path

# 2. Generate quote from Gemini

def generate_quote():
    topics = ["motivation", "success", "resilience", "self-discipline", "consistency"]
    seed = random.randint(1000, 9999)  # simple entropy
    prompt = f"Give me one original motivational quote inside double quotes related to {random.choice(topics)}. Just the quote. Seed:{seed}"
    
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip().strip('"')

# 3. Render the quote on the image
def create_image_with_quote(quote, background_path="background.jpg", output_path="daily-quote.jpg"):
    img = Image.open(background_path).convert("RGB")
    
    # Step 1: Compute average brightness
    grayscale = img.convert("L")  # L mode = grayscale
    avg_brightness = sum(grayscale.getdata()) / (grayscale.width * grayscale.height)
    
    # Step 2: Choose text color based on brightness
    text_color = "white" if avg_brightness < 128 else "black"
    print(f"🖌️ Using text color: {text_color} (brightness = {avg_brightness:.2f})")

    draw = ImageDraw.Draw(img)

    # Load custom high-res font
    try:
        font = ImageFont.truetype("fonts/Poppins-Regular.ttf", size=60)
    except:
        font = ImageFont.load_default()

    # Word wrap across full width
    wrapped = textwrap.fill(quote, width=22)
    lines = wrapped.split("\n")
    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)
    y_start = (img.height - total_height) // 2

    for line in lines:
        line_width = draw.textbbox((0, 0), line, font=font)[2]
        x = (img.width - line_width) // 2
        draw.text((x, y_start), line, font=font, fill=text_color)
        y_start += font.size + 12

    img.save(output_path)
    print(f"✅ Saved polished quote image as {output_path}")


# Full pipeline
if __name__ == "__main__":
    quote = generate_quote()
    bg_path = get_blurred_background(topic="inspiration")
    create_image_with_quote(quote, background_path=bg_path)

    bot = Bot(base_path="/tmp/instabot/")

    bot.login(username=USERNAME, password=PASSWORD)
    bot.upload_photo("daily-quote.jpg", caption="💡 Stay inspired! #motivation")
