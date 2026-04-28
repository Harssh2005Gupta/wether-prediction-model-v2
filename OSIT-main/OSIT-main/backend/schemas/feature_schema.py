# schemas/feature_schema.py

from pydantic import BaseModel

class FeatureInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float