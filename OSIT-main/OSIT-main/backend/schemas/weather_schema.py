# schemas/weather_schema.py

from pydantic import BaseModel

class WeatherData(BaseModel):
    temperature: float
    humidity: float
    rainfall: float
    rain_probability: float