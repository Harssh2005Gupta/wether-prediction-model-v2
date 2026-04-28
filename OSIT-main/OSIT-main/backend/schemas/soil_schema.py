# schemas/soil_schema.py

from pydantic import BaseModel

class SoilData(BaseModel):
    N: float
    P: float
    K: float
    ph: float