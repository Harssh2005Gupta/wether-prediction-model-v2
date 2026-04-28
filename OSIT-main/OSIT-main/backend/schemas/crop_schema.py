# schemas/crop_schema.py

from pydantic import BaseModel
from typing import List

class CropRecommendation(BaseModel):
    crop: str
    confidence: float

class CropOutput(BaseModel):
    recommendations: List[CropRecommendation]