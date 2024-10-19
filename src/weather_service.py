import requests
import logging
from datetime import datetime, timezone
import numpy as np
from weather_db_mysql import insert_summaries

from tenacity import retry, stop_after_attempt, wait_exponential



# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherService:
    def __init__(self, api_key: str, locations: list[str]):
        self.api_key = api_key
        self.locations = locations
        self.daily_summary = {}
        self.forecast_summary = {}

    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_weather_data(self):
        weather_data = {}
        for location in self.locations:
            try:
                response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric')
                response.raise_for_status()
                data = response.json()
                if 'main' in data:
                    weather_data[location] = data
                else:
                    logging.error(f"'main' key not found in the response for location: {location}")
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error occurred for {location}: {e}")
            except Exception as e:
                logging.error(f"An error occurred for {location}: {e}")
        return weather_data

    def fetch_forecast_data(self):
        forecast_data = {}
        for location in self.locations:
            try:
                response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={self.api_key}&units=metric')
                response.raise_for_status()
                forecast_data[location] = response.json()
                self.log_success(location, "forecast data")
            except requests.RequestException as e:
                self.log_error(location, "forecast data", e)
        return forecast_data

    def log_success(self, location: str, data_type: str):
        logging.info(f"Successfully fetched {data_type} for {location}")

    def log_error(self, location: str, data_type: str, error: Exception):
        logging.error(f"Request error for {data_type} in {location}: {error}")

    def process_weather_data(self, data: dict):
        self.daily_summary.clear()
        for location, weather in data.items():
            self.extract_weather_summary(location, weather)

    def extract_weather_summary(self, location: str, weather: dict):
        try:
            logging.info(f"Processing weather data for {location}: {weather}")
            main_data = weather.get('main', {})
            wind_data = weather.get('wind', {})
            weather_data = weather.get('weather', [{}])[0]

            # Extracting weather metrics with error handling
            temperature = main_data.get('temp')
            humidity = main_data.get('humidity')
            wind_speed = wind_data.get('speed')
            weather_description = weather_data.get('main')

            if None in (temperature, humidity, wind_speed, weather_description):
                logging.error(f"Data processing error: Missing expected weather data for {location}")
                return

            timestamp = datetime.now(tz=timezone.utc).date()
            if timestamp not in self.daily_summary:
                self.daily_summary[timestamp] = {
                    'temperatures': [],
                    'humidities': [],
                    'wind_speeds': [],
                    'conditions': []
                }

            self.daily_summary[timestamp]['temperatures'].append(temperature)
            self.daily_summary[timestamp]['humidities'].append(humidity)
            self.daily_summary[timestamp]['wind_speeds'].append(wind_speed)
            self.daily_summary[timestamp]['conditions'].append(weather_description)

            self.update_daily_summary(timestamp)
        except Exception as e:
            logging.error(f"Unexpected error while extracting weather summary: {e}")

    def update_daily_summary(self, timestamp: datetime.date):
        summary = self.daily_summary[timestamp]
        summary['average_temp'] = np.mean(summary['temperatures'])
        summary['max_temp'] = np.max(summary['temperatures'])
        summary['min_temp'] = np.min(summary['temperatures'])
        summary['average_humidity'] = np.mean(summary['humidities'])
        summary['average_wind_speed'] = np.mean(summary['wind_speeds'])
        summary['dominant_condition'] = max(set(summary['conditions']), key=summary['conditions'].count)

    def process_forecast_data(self, data: dict):
        self.forecast_summary.clear()
        for location, forecast in data.items():
            self.extract_forecast_summary(location, forecast)

    def extract_forecast_summary(self, location: str, forecast: dict):
        try:
            for entry in forecast['list']:
                forecast_time = datetime.fromtimestamp(entry['dt'], tz=timezone.utc).date()
                temp = entry['main']['temp']
                humidity = entry['main']['humidity']
                wind_speed = entry['wind']['speed']
                condition = entry['weather'][0]['main']

                if forecast_time not in self.forecast_summary:
                    self.forecast_summary[forecast_time] = {}
                if location not in self.forecast_summary[forecast_time]:
                    self.forecast_summary[forecast_time][location] = {
                        'temperatures': [],
                        'humidities': [],
                        'wind_speeds': [],
                        'conditions': []
                    }

                self.forecast_summary[forecast_time][location]['temperatures'].append(temp)
                self.forecast_summary[forecast_time][location]['humidities'].append(humidity)
                self.forecast_summary[forecast_time][location]['wind_speeds'].append(wind_speed)
                self.forecast_summary[forecast_time][location]['conditions'].append(condition)

            self.update_forecast_summary()
        except KeyError as e:
            logging.error(f"Data processing error in forecast data: Missing key {e}")

    def update_forecast_summary(self):
        today = datetime.now(tz=timezone.utc).date()
        if today in self.forecast_summary:
            for location, summary in self.forecast_summary[today].items():
                temperatures = summary['temperatures']
                humidities = summary['humidities']
                wind_speeds = summary['wind_speeds']
                conditions = summary['conditions']
                for temp, humidity, wind_speed, condition in zip(temperatures, humidities, wind_speeds, conditions):
                    insert_summaries([(today.strftime('%Y-%m-%d'), location, temp, humidity, wind_speed, condition)])

if __name__ == "__main__":
    config = {
        "API_KEY": "6d01d8032b8b2e700a1279d7bbba7a51",
        "LOCATIONS": ['New York', 'Los Angeles', 'Chicago']
    }

    weather_service = WeatherService(config["API_KEY"], config["LOCATIONS"])

    current_weather = weather_service.fetch_weather_data()
    weather_service.process_weather_data(current_weather)

    forecast_data = weather_service.fetch_forecast_data()
    weather_service.process_forecast_data(forecast_data)
