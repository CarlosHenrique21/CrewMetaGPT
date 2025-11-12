from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Location:
    city_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    user_label: Optional[str] = None

@dataclass
class DailyForecast:
    date: datetime
    temperature: float
    humidity: int
    wind_speed: float
    condition_description: str

@dataclass
class WeatherData:
    temperature: float
    humidity: int
    wind_speed: float
    condition_description: str
    uv_index: Optional[int] = None
    sunrise_time: Optional[datetime] = None
    sunset_time: Optional[datetime] = None
    forecast_days: List[DailyForecast] = field(default_factory=list)
