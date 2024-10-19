import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from weather_monitor import check_temperature_alert, parse_arguments
from weather_service import WeatherService

class TestWeatherMonitor(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(locations=['New York', 'Los Angeles'], threshold=35)
        args = parse_arguments()
        self.assertEqual(args.locations, ['New York', 'Los Angeles'])
        self.assertEqual(args.threshold, 35)

    def test_check_temperature_alert(self):
        test_data = {
            'New York': {'main': {'temp': 30}},
            'Los Angeles': {'main': {'temp': 40}},
            'Chicago': {'main': {'temp': 20}},
        }
        threshold = 35
        alerts = check_temperature_alert(test_data, threshold)
        self.assertEqual(alerts, ["Alert! Los Angeles has reached 40°C, exceeding the threshold of 35°C."])

    def test_check_temperature_alert_no_alert(self):
        test_data = {
            'New York': {'main': {'temp': 30}},
            'Los Angeles': {'main': {'temp': 32}},
            'Chicago': {'main': {'temp': 20}},
        }
        threshold = 35
        alerts = check_temperature_alert(test_data, threshold)
        self.assertEqual(alerts, [])

    def test_check_temperature_alert_missing_data(self):
        test_data = {
            'New York': {'main': {'temp': 30}},
            'Los Angeles': {},
            'Chicago': {'main': {'temp': 20}},
        }
        threshold = 35
        with self.assertLogs('root', level='ERROR') as log:
            alerts = check_temperature_alert(test_data, threshold)
            self.assertIn("Temperature data not available for Los Angeles.", log.output[0])
        self.assertEqual(alerts, [])

    @patch('weather_service.requests.get')
    def test_fetch_weather_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'main': {'temp': 36}}
        mock_get.return_value = mock_response

        api_key = '6d01d8032b8b2e700a1279d7bbba7a51'
        locations = ['New York']
        weather_service = WeatherService(api_key, locations)

        data = weather_service.fetch_weather_data()
        self.assertEqual(data, {'New York': {'main': {'temp': 36}}})

    @patch('weather_service.requests.get')
    def test_fetch_forecast_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'list': [
                {'dt': 1609459200, 'main': {'temp': 20}, 'weather': [{'main': 'Clear'}]},
                {'dt': 1609545600, 'main': {'temp': 22}, 'weather': [{'main': 'Cloudy'}]},
            ]
        }
        mock_get.return_value = mock_response

        api_key = '6d01d8032b8b2e700a1279d7bbba7a51'
        locations = ['New York']
        weather_service = WeatherService(api_key, locations)

        forecast_data = weather_service.fetch_forecast_data()
        self.assertIn('New York', forecast_data)

if __name__ == "__main__":
    unittest.main()
