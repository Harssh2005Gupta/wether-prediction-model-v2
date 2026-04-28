# schemas/input_schema.py

from pydantic import BaseModel
from typing import Optional

class UserInput(BaseModel):
    lat: float
    lon: float
    
    # Optional manual overrides
    N: Optional[float] = None
    P: Optional[float] = None
    K: Optional[float] = None
    ph: Optional[float] = None

    # Optional image for disease detection
    image: Optional[str] = None

    # Optional language preference
    language: Optional[str] = "English"