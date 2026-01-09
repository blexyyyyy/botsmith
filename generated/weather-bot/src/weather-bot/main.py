# src/weather-bot/main.py

from services.weather_service import WeatherService
from config import settings

def main() -> None:
    """
    Entry point for the weather bot.
    Fetches weather data and prints results.
    """
    try:
        weather_service = WeatherService(settings.api_key, settings.city)
        weather_data = weather_service.fetch_weather()
        print(weather_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()