# Weather Bot

Welcome to the Weather Bot project! This bot allows you to check the weather in any city around the world using simple commands.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Contribution](#contribution)
8. [License](#license)

## Overview

The Weather Bot is a Python-based application that integrates with the OpenWeatherMap API to provide real-time weather updates and forecasts. It can be used in various platforms such as Telegram, Slack, and more.

## Features

- **Real-Time Weather Data**: Get current weather conditions for any city.
- **Forecast**: Receive up to 5-day weather forecasts.
- **Location Support**: Search by city name or coordinates.
- **Customizable Responses**: Tailor your bot's output to fit your needs.

## Requirements

To run the Weather Bot, you will need:

- Python 3.8 or higher
- An OpenWeatherMap API key (sign up at [OpenWeatherMap](https://openweathermap.org/) and generate an API key)
- A compatible messaging platform (e.g., Telegram, Slack)

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/weather-bot.git
   cd weather-bot
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   Create a `.env` file in the project root and add your OpenWeatherMap API key:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```

## Usage

### Running the Bot

1. **Run the Bot Script**:
   ```sh
   python bot.py
   ```

2. **Connect to Messaging Platform**:
   Follow the instructions provided in the terminal to connect your bot to a messaging platform.

### Commands

- `/weather <city>`: Get current weather for a specified city.
- `/forecast <city>`: Get 5-day weather forecast for a specified city.
- `/help`: Display available commands and their usage.

## Configuration

The bot can be customized by editing the `config.py` file:

```python
# config.py

# Bot configuration settings
TOKEN = 'your_bot_token_here'  # Your bot token from the messaging platform
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')  # OpenWeatherMap API key
```

## Contribution

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Thank you for using the Weather Bot!