# schemas/llm_schema.py

from pydantic import BaseModel
from typing import List

class LLMCrop(BaseModel):
    crop: str
    reason: str

class LLMOutput(BaseModel):
    explanation: str
    top_crops: List[LLMCrop]