import os
from typing import Optional

class Settings:
    """
    Configuration settings for the Weather Bot.
    """

    def __init__(self):
        self.api_key: str = os.getenv("WEATHER_API_KEY", "")
        self.city: str = os.getenv("DEFAULT_CITY", "New York")
        self.temperature_unit: str = os.getenv("TEMPERATURE_UNIT", "Celsius")

settings = Settings()