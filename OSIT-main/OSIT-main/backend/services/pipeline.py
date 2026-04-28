# services/pipeline.py

from features.log_lat import FarmAnalyzer
from features.agent import recommend_crops, merge_recommendations
from features.llm_recommendation import llm_recommend
from features.doctor import detect_disease


# =========================
# ALERT ENGINE
# =========================
def generate_alerts(features: dict):
    alerts = []

    if features["rainfall"] < 5:
        alerts.append("🌱 Low rainfall expected - irrigation required")

    if features["temperature"] > 40:
        alerts.append("🔥 Heatwave alert - protect crops")

    if features.get("rain_probability", 0) > 0.7:
        alerts.append("🌧 Heavy rain expected - avoid irrigation")

    if features["humidity"] > 85:
        alerts.append("⚠️ High humidity - risk of fungal diseases")

    return alerts


# =========================
# MAIN PIPELINE
# =========================
def run_pipeline(user_input: dict):
    """
    Full AI pipeline:
    Weather + Soil → Features → ML → LLM → Disease → Alerts
    """

    # =========================
    # 1. Fetch Data (Weather + Soil)
    # =========================
    analyzer = FarmAnalyzer(user_input["lat"], user_input["lon"])
    analyzer.fetch_all()

    features = analyzer.get_features()

    # Override with user values if provided
    for key in ["N", "P", "K", "ph"]:
        if user_input.get(key) is not None:
            features[key] = user_input[key]

    # =========================
    # 2. ML Crop Recommendation
    # =========================
    ml_output = recommend_crops(features)

    # =========================
    # 3. LLM Recommendation
    # =========================
    llm_output = llm_recommend(features)

    # =========================
    # 4. Merge ML + LLM
    # =========================
    merged = merge_recommendations(ml_output, llm_output)

    # =========================
    # 5. Disease Detection (Optional)
    # =========================
    disease_result = None

    if user_input.get("image"):
        disease_result = detect_disease(user_input["image"])

    # =========================
    # 6. Alerts
    # =========================
    alerts = generate_alerts(features)

    # =========================
    # 7. Final Response
    # =========================
    return {
        "final_crops": merged["final_crops"],
        "ml_recommendations": merged["ml"],
        "llm_recommendations": merged["llm"],
        "advisory": merged.get("explanation", ""),
        "disease": disease_result,
        "alerts": alerts
    }