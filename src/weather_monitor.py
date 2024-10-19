import logging
import argparse
from src.weather_service import WeatherService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Weather Monitoring System')
    parser.add_argument('--locations', type=str, nargs='+', help='List of locations to monitor', required=True)
    parser.add_argument('--threshold', type=int, default=35, help='Temperature threshold for alerts')
    return parser.parse_args()

def check_temperature_alert(weather_data, threshold):
    alerts = []
    for location, data in weather_data.items():
        try:
            temp = data['main']['temp']
            if temp > threshold:
                alerts.append(f"Alert! {location} has reached {temp}°C, exceeding the threshold of {threshold}°C.")
        except KeyError:
            logging.error(f"Temperature data not available for {location}.")
    return alerts

def test_temperature_alerts():
    test_data = {
        'New York': {'main': {'temp': 30}},
        'Los Angeles': {'main': {'temp': 40}},
        'Chicago': {'main': {'temp': 20}},
    }
    threshold = 35
    alerts = check_temperature_alert(test_data, threshold)
    assert alerts == ["Alert! Los Angeles has reached 40°C, exceeding the threshold of 35°C."]

if __name__ == "__main__":
    args = parse_arguments()
    locations = args.locations
    temperature_threshold = args.threshold
    api_key = "6d01d8032b8b2e700a1279d7bbba7a51"

    weather_data = {}
    weather_service = WeatherService(api_key, locations)

    for location in locations:
        data = weather_service.fetch_weather_data(location) 
        if data:
            weather_data[location] = data  
        else:
            logging.warning(f"Failed to fetch weather data for {location}.")

    alerts = check_temperature_alert(weather_data, temperature_threshold)
    for alert in alerts:
        print(alert)

    print(f"Monitoring locations: {locations} with a temperature threshold of {temperature_threshold}°C")

    test_temperature_alerts()
