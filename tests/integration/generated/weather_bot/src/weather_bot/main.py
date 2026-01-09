from weather_bot.services.weather_service import WeatherService

def main() -> None:
    """
    Entry point for the weather bot. Fetches weather data and prints results.
    """
    try:
        weather_service = WeatherService()
        weather_data = weather_service.fetch_weather()
        if weather_data:
            print(weather_data)
        else:
            print("Failed to retrieve weather data.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
