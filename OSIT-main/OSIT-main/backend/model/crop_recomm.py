import os
import pickle
import numpy as np

# =========================
# Load model safely
# =========================

model_path = os.path.join(os.path.dirname(__file__), "crop_recommendation.sav")

with open(model_path, "rb") as f:
    model = pickle.load(f)


# =========================
# Prediction Function
# =========================

def predict_crop(data: dict):
    """
    Predict crop using dictionary input

    Expected keys:
    N, P, K, temperature, humidity, ph, rainfall
    """

    try:
        features = [
            data["N"],
            data["P"],
            data["K"],
            data["temperature"],
            data["humidity"],
            data["ph"],
            data["rainfall"]
        ]

        input_array = np.array(features).reshape(1, -1)

        prediction = model.predict(input_array)[0]

        return {
            "crop": prediction
        }

    except KeyError as e:
        return {"error": f"Missing feature: {str(e)}"}

    except Exception as e:
        return {"error": str(e)}