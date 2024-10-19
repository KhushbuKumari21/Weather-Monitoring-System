import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.alert_service import AlertService

class TestAlertService(unittest.TestCase):
    def setUp(self):
        self.alert_service = AlertService()

    def test_temperature_alert(self):
        weather_data = {
            'CityA': {
                'main': {'temp': 310, 'humidity': 60},
                'wind': {'speed': 10}
            }
        }
        alerts_first_call = self.alert_service.check_alerts(weather_data)
        alerts_second_call = self.alert_service.check_alerts(weather_data)
        self.assertIn("Alert! CityA temperature exceeded 35°C for consecutive updates.", alerts_second_call)

    def test_humidity_alert(self):
        weather_data = {
            'CityB': {
                'main': {'temp': 298, 'humidity': 90},
                'wind': {'speed': 8}
            }
        }
        alerts = self.alert_service.check_alerts(weather_data)
        self.assertIn("Alert! CityB humidity exceeded 80%.", alerts)

    def test_wind_speed_alert(self):
        weather_data = {
            'CityC': {
                'main': {'temp': 295, 'humidity': 55},
                'wind': {'speed': 20}
            }
        }
        alerts = self.alert_service.check_alerts(weather_data)
        self.assertIn("Alert! CityC wind speed exceeded 15 m/s.", alerts)

    def test_no_alert_scenario(self):
        weather_data = {
            'CityD': {
                'main': {'temp': 298, 'humidity': 60},
                'wind': {'speed': 8}
            }
        }
        alerts = self.alert_service.check_alerts(weather_data)
        self.assertEqual(alerts, [])

    def test_single_alert_reset(self):
        weather_data_exceed = {
            'CityE': {
                'main': {'temp': 310, 'humidity': 60},
                'wind': {'speed': 10}
            }
        }
        weather_data_normal = {
            'CityE': {
                'main': {'temp': 300, 'humidity': 60},
                'wind': {'speed': 10}
            }
        }
        self.alert_service.check_alerts(weather_data_exceed)
        alerts_after_reset = self.alert_service.check_alerts(weather_data_normal)
        self.assertEqual(alerts_after_reset, [])

if __name__ == '__main__':
    unittest.main()
