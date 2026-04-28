# features/plant_disease.py

from google import genai
from PIL import Image
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Load API key safely
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)


def detect_disease(image_path: str):
    """
    Detect plant disease from image and return structured report
    """

    if not image_path:
        return {"error": "No image provided"}

    try:
        img = Image.open(image_path)
    except Exception as e:
        return {"error": f"Image error: {str(e)}"}

    prompt = """
    You are an AI Agriculture Expert.

    Analyze the plant image and return:
    1. Disease name (or 'Healthy')
    2. Confidence level
    3. Causes
    4. Treatment steps
    5. Prevention tips

    Respond strictly in JSON format.
    """

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-pro"),
            contents=[prompt, img],
            config={
                "response_mime_type": "application/json",
            },
        )

        result = json.loads(response.text)

        return result

    except Exception as e:
        return {"error": f"API error: {str(e)}"}