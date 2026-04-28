# features/llm_recommendation.py

import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

_llm = None


# =========================
# LLM Loader (Lazy)
# =========================
def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-pro"),
            temperature=0.2
        )
    return _llm


# =========================
# LLM Crop Recommendation
# =========================
def llm_recommend(input_data: dict) -> dict:
    """
    Returns structured crop recommendations from LLM
    """

    prompt_template = ChatPromptTemplate.from_template("""
    You are an expert agricultural advisor.

    Based on the following soil and climate data:

    Nitrogen: {N}
    Phosphorus: {P}
    Potassium: {K}
    Temperature: {temperature} °C
    Humidity: {humidity} %
    Soil pH: {ph}
    Rainfall: {rainfall} mm

    Respond ONLY in valid JSON.

    Format:
    {{
      "explanation": "short paragraph",
      "top_crops": [
        {{"crop": "name", "reason": "why suitable"}},
        {{"crop": "name", "reason": "why suitable"}},
        {{"crop": "name", "reason": "why suitable"}}
      ]
    }}
    """)

    llm = _get_llm()
    prompt = prompt_template.format_messages(**input_data)

    try:
        response = llm.invoke(prompt)
        content = response.content.strip()

        # 🔹 Clean markdown if present
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:].strip()

        # 🔹 Extract JSON safely
        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("No JSON found in response")

        json_str = content[start:end]

        result = json.loads(json_str)

        # 🔹 Normalize output (VERY IMPORTANT)
        if "top_crops" not in result:
            result["top_crops"] = []

        return result

    except Exception as e:
        return {
            "error": str(e),
            "top_crops": [],
            "explanation": "Could not generate recommendation"
        }