# schemas/disease_schema.py

from pydantic import BaseModel
from typing import List, Optional

class DiseaseOutput(BaseModel):
    disease: Optional[str]
    confidence: Optional[float]
    causes: Optional[List[str]]
    treatment: Optional[List[str]]
    prevention: Optional[List[str]]