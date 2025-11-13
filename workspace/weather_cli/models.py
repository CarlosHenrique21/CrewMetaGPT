from dataclasses import dataclass
from datetime import datetime
@dataclass
class Weather:
    location: str
    temperature: float
    humidity: float
    wind_speed: float
    forecast: list  # List of daily forecast items
    retrieved_at: datetime