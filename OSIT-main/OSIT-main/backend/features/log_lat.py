import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


class FarmAnalyzer:
    SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"
    OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
        self.soil_data = None
        self.weather_data = None

    # ----------------- Fetchers -----------------
    def fetch_soil_data(self) -> dict:
        params = {
            "lon": self.lon,
            "lat": self.lat,
            "property": ["phh2o", "soc", "clay", "sand", "nitrogen", "cec", "bdod"]
        }
        try:
            resp = requests.get(self.SOILGRIDS_URL, params=params, timeout=30)
            resp.raise_for_status()
            self.soil_data = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"[WARN] Could not fetch soil data: {e}")
            # Fallback default values
            self.soil_data = {
                "properties": {
                    "layers": [
                        {"name": "phh2o", "depths": [{"values": {"mean": 6.5}}]},
                        {"name": "soc", "depths": [{"values": {"mean": 1.2}}]},
                        {"name": "clay", "depths": [{"values": {"mean": 25}}]},
                        {"name": "sand", "depths": [{"values": {"mean": 45}}]},
                        {"name": "nitrogen", "depths": [{"values": {"mean": 8}}]},
                        {"name": "cec", "depths": [{"values": {"mean": 15}}]},
                        {"name": "bdod", "depths": [{"values": {"mean": 1.2}}]}
                    ]
                }
            }
        return self.soil_data

    def fetch_weather_data(self) -> dict:
        try:
            self.weather_data = self._fetch_openweather()
        except Exception:
            try:
                self.weather_data = self._fetch_weather_open_meteo()
            except Exception as e2:
                print(f"[WARN] Could not fetch weather data: {e2}")
                self.weather_data = {
                    "current": {"temp": 22.5, "humidity": 65},
                    "daily": [{"rain": 2.5}]
                }
        return self.weather_data

    # ----------------- Private helpers -----------------
    def _fetch_openweather(self):
        if not self.OPENWEATHER_API_KEY:
            raise Exception("API key missing")

        url = "https://api.openweathermap.org/data/3.0/onecall"

        params = {
            "lat": self.lat,
            "lon": self.lon,
            "exclude": "minutely,alerts",
            "appid": self.OPENWEATHER_API_KEY,
            "units": "metric"
        }

        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()

        data = resp.json()

        return {
            "temperature": data["current"]["temp"],
            "humidity": data["current"]["humidity"],
            "rainfall": data.get("daily", [{}])[0].get("rain", 0),
            "rain_probability": data.get("daily", [{}])[0].get("pop", 0)  # 🔥 NEW
        }
    def _fetch_weather_open_meteo(self) -> dict:
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current": "temperature_2m,relative_humidity_2m",
            "daily": "rain_sum",
            "forecast_days": 1,
            "timezone": "auto",
        }
        resp = requests.get(self.OPEN_METEO_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            "current": {
                "temp": data.get("current", {}).get("temperature_2m"),
                "humidity": data.get("current", {}).get("relative_humidity_2m"),
            },
            "daily": [{"rain": (data.get("daily", {}).get("rain_sum", [0]) or [0])[0]}],
        }

    def _get_soil_property(self, name: str, default=0):
        if not self.soil_data:
            return default
        layers = self.soil_data.get("properties", {}).get("layers", [])
        for layer in layers:
            if layer.get("name") == name:
                d_factor = layer.get("unit_measure", {}).get("d_factor", 1) or 1
                for depth in layer.get("depths", []):
                    mean_val = depth.get("values", {}).get("mean")
                    if mean_val is not None:
                        return mean_val / d_factor if d_factor != 1 else mean_val
        return default

    # ----------------- Public Getters -----------------
    def get_ph_value(self): return self._get_soil_property("phh2o", default=6.5)
    def get_nitrogen_value(self): return self._get_soil_property("nitrogen", default=8)
    def get_soc_value(self): return self._get_soil_property("soc", default=1.2)
    def get_clay_value(self): return self._get_soil_property("clay", default=25)
    def get_sand_value(self): return self._get_soil_property("sand", default=45)
    def get_cec_value(self): return self._get_soil_property("cec", default=15)
    def get_bdod_value(self): return self._get_soil_property("bdod", default=1.2)

    def get_temperature(self):
        if not self.weather_data:
            self.fetch_weather_data()
        return self.weather_data.get("current", {}).get("temp", 22.5)

    def get_humidity(self):
        if not self.weather_data:
            self.fetch_weather_data()
        return self.weather_data.get("current", {}).get("humidity", 65)

    def get_rainfall(self):
        if not self.weather_data:
            self.fetch_weather_data()
        return self.weather_data.get("daily", [{}])[0].get("rain", 0)

    # ----------------- Analysis -----------------
    def analyze_and_report(self) -> str:
        self.fetch_soil_data()
        self.fetch_weather_data()
        report = [
            "**Soil Report**",
            f"- pH: {self.get_ph_value()}",
            f"- Organic Carbon (SOC): {self.get_soc_value()}",
            f"- Nitrogen: {self.get_nitrogen_value()}",
            f"- Clay: {self.get_clay_value()}%",
            f"- Sand: {self.get_sand_value()}%",
            f"- Bulk Density (bdod): {self.get_bdod_value()}",
            f"- Cation Exchange Capacity (CEC): {self.get_cec_value()}",
            "",
            "🌦 **Weather Report**",
            f"- Temperature: {self.get_temperature()}°C",
            f"- Humidity: {self.get_humidity()}%",
            f"- Expected Rainfall Today: {self.get_rainfall()} mm",
        ]
        if self.get_nitrogen_value() < 10:
            report.append("👉 Add nitrogen fertilizer.")
        if self.get_ph_value() < 5.5:
            report.append("👉 Soil is acidic, consider adding lime.")
        if self.get_rainfall() < 5:
            report.append("👉 Irrigation needed (low rainfall).")
        return "\n".join(report)

    def get_features_dict(self) -> dict:
        # Return safe numeric defaults if data missing
        return {
            "N": self.get_nitrogen_value(),
            "P": 10,  # Placeholder default
            "K": 10,  # Placeholder default
            "temperature": self.get_temperature(),
            "humidity": self.get_humidity(),
            "ph": self.get_ph_value(),
            "rainfall": self.get_rainfall()
        }

    # ----------------- Convenience Aliases -----------------
    def fetch_all(self):
        """Fetch both soil and weather data in one call."""
        self.fetch_soil_data()
        self.fetch_weather_data()

    def get_features(self) -> dict:
        """Alias for get_features_dict — used by pipeline and API endpoints."""
        return self.get_features_dict()
