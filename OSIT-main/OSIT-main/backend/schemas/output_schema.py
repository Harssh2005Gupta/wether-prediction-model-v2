# schemas/output_schema.py

from pydantic import BaseModel
from typing import List, Optional
from schemas.crop_schema import CropRecommendation

class FinalOutput(BaseModel):
    final_crops: List[str]

    ml_recommendations: List[str]
    llm_recommendations: List[str]

    advisory: str

    disease: Optional[dict] = None

    alerts: List[str]