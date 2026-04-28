# features/agent.py

import os
import numpy as np
import pandas as pd
import joblib


# =========================
# Load models safely
# =========================

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "crop_recommendation.sav")

import pickle
with open(MODEL_PATH, "rb") as f:
    pipeline = pickle.load(f)

# =========================
# ML Recommendation
# =========================

def recommend_crops(input_dict, top_n=3):
    """
    Returns top-N crops with probabilities
    """
    keys = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    features = [input_dict[k] for k in keys]
    input_array = np.array(features).reshape(1, -1)

    probs = pipeline.predict_proba(input_array)[0]

    sorted_idx = np.argsort(probs)[::-1][:top_n]

    crops = pipeline.classes_[sorted_idx]

    return {
        "recommendations": [
            {"crop": crop, "confidence": float(probs[idx])}
            for crop, idx in zip(crops, sorted_idx)
        ]
    }


# =========================
# Merge ML + LLM
# =========================

def merge_recommendations(ml_output, llm_output, top_n=3):
    """
    Combine ML + LLM intelligently
    """

    ml_crops = [c["crop"] for c in ml_output["recommendations"]]

    llm_crops = []
    if "recommendations" in llm_output:
        llm_crops = [c["crop_name"] for c in llm_output["recommendations"]]
    elif "top_crops" in llm_output:
        llm_crops = [c["crop"] for c in llm_output["top_crops"]]

    # 1. Common crops
    common = [c for c in ml_crops if c in llm_crops]

    # 2. Fill remaining from ML
    final = common[:]
    for crop in ml_crops:
        if crop not in final:
            final.append(crop)
        if len(final) >= top_n:
            break

    return {
        "final_crops": final,
        "ml": ml_crops,
        "llm": llm_crops,
        "explanation": llm_output.get("summary", "")
    }