# Python Weather Bot

## Overview

The Python Weather Bot is a command-line application designed to fetch and display weather information for specified locations. This bot utilizes the OpenWeatherMap API to retrieve real-time weather data.

## Features

- Fetch current weather conditions for any location.
- Display temperature, humidity, wind speed, and more.
- Support for multiple cities by entering their names.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.6 or later installed on your system.
- An API key from OpenWeatherMap to access weather data. You can obtain an API key by signing up at [OpenWeatherMap](https://openweathermap.org/).

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/python-weather-bot.git
   cd python-weather-bot
   ```

2. **Create a Virtual Environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install requests
   ```

## Configuration

1. **Set Up API Key:**
   Rename the `.env.example` file to `.env` and add your OpenWeatherMap API key:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```

2. **Install `python-dotenv`:**
   ```bash
   pip install python-dotenv
   ```

## Usage

1. **Run the Bot:**
   ```bash
   python weather_bot.py
   ```

2. **Enter a Location:**
   When prompted, enter the name of the city for which you want to check the weather.

3. **View Weather Information:**
   The bot will display the current weather conditions for the specified location.

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact us at [your-email@example.com] or open an issue on the [GitHub repository](https://github.com/yourusername/python-weather-bot).