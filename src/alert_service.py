import logging

class AlertService:
    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {
            'temperature': 35,
            'humidity': 80,
            'wind_speed': 15
        }
        self.previous_exceed = {}

    def set_threshold(self, condition, value):
        self.thresholds[condition] = value

    def kelvin_to_celsius(self, kelvin):
        return kelvin - 273.15

    def kelvin_to_fahrenheit(self, kelvin):
        return (kelvin - 273.15) * 9/5 + 32

    def check_alerts(self, weather_data, temp_unit='C'):
        alerts = []
        for location, weather in weather_data.items():
            temp_k = weather.get('main', {}).get('temp')
            if temp_k is not None:
                temp = (self.kelvin_to_celsius(temp_k) if temp_unit == 'C' 
                        else self.kelvin_to_fahrenheit(temp_k))
            else:
                temp = None
            
            humidity = weather.get('main', {}).get('humidity')
            wind_speed = weather.get('wind', {}).get('speed')

            if temp is None:
                logging.error(f"Data processing error: Missing key 'temp' for {location}. Skipping this entry.")
                continue
            if humidity is None:
                logging.error(f"Data processing error: Missing key 'humidity' for {location}. Skipping this entry.")
                continue
            if wind_speed is None:
                logging.error(f"Data processing error: Missing key 'wind_speed' for {location}. Skipping this entry.")
                continue

            if temp > self.thresholds['temperature']:
                if self.previous_exceed.get(location, {}).get('temperature', False):
                    alert_message = f"Alert! {location} temperature exceeded {self.thresholds['temperature']}°C for consecutive updates."
                    alerts.append(alert_message)
                    logging.info(alert_message)
                self.previous_exceed.setdefault(location, {})['temperature'] = True
            else:
                self.previous_exceed.setdefault(location, {})['temperature'] = False
            
            if humidity > self.thresholds['humidity']:
                alert_message = f"Alert! {location} humidity exceeded {self.thresholds['humidity']}%."
                alerts.append(alert_message)
                logging.info(alert_message)

            if wind_speed > self.thresholds['wind_speed']:
                alert_message = f"Alert! {location} wind speed exceeded {self.thresholds['wind_speed']} m/s."
                alerts.append(alert_message)
                logging.info(alert_message)

        return alerts

    def send_alert(self, message):
        logging.info(f"Sending alert: {message}")

    def evaluate_alerts(self, weather_data, temp_unit='C'):
        alerts = self.check_alerts(weather_data, temp_unit)
        for alert in alerts:
            self.send_alert(alert)
