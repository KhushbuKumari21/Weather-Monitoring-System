import time
import json
import logging
import requests  
from src.weather_service import WeatherService
from src.alert_service import AlertService
from src.visualization import Visualization

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

API_KEY = config['API_KEY']
LOCATIONS = config['LOCATIONS']
INTERVAL = config['INTERVAL']
DURATION = config.get('DURATION', None)

logging.basicConfig(filename='weather_monitoring.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    weather_service = WeatherService(API_KEY, LOCATIONS)
    alert_service = AlertService()
    visualization = Visualization()

    start_time = time.time()
    
    while True:
        try:
            weather_data = weather_service.fetch_weather_data()
            forecast_data = weather_service.fetch_forecast_data()
            weather_service.process_weather_data(weather_data)
            weather_service.process_forecast_data(forecast_data)

            alerts = alert_service.check_alerts(weather_data)
            if alerts:
                logging.warning("Alerts triggered: %s", alerts)

            visualization.display_summary(weather_service.daily_summary)
            visualization.display_forecast_summary(weather_service.forecast_summary)

        except (requests.ConnectionError, requests.Timeout) as e:
            logging.error("Network error occurred: %s", str(e))
            time.sleep(INTERVAL)

        except json.JSONDecodeError as e:
            logging.error("Failed to parse JSON data: %s", str(e))
            time.sleep(INTERVAL)

        except Exception as e:
            logging.error("An unexpected error occurred: %s", str(e))
            continue

        
        if DURATION and (time.time() - start_time) > DURATION:
            logging.info("Monitoring ended after specified duration of %s seconds.", DURATION)
            break

        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()
