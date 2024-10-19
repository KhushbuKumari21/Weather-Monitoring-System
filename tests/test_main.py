import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import json
import time
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from main import main

class TestWeatherMonitoring(unittest.TestCase):
    @patch('src.main.WeatherService')
    @patch('src.main.AlertService')
    @patch('src.main.Visualization')
    @patch('src.main.json.load')
    @patch('src.main.open')
    @patch('src.main.logging')
    def test_main_function_with_fetch_error(self, mock_logging, mock_open, mock_json_load, mock_Visualization, mock_AlertService, mock_WeatherService):
        mock_config = {
            'API_KEY': 'mock_api_key',
            'LOCATIONS': ['Delhi', 'Mumbai'],
            'INTERVAL': 300,
            'DURATION': 600
        }
        mock_json_load.return_value = mock_config
        mock_weather_service = MagicMock()
        mock_WeatherService.return_value = mock_weather_service
        mock_weather_service.fetch_weather_data.side_effect = Exception("Network error")
        mock_alert_service = MagicMock()
        mock_AlertService.return_value = mock_alert_service
        mock_alert_service.check_alerts.return_value = []
        mock_visualization = MagicMock()
        mock_Visualization.return_value = mock_visualization
        with patch('src.main.time.sleep', return_value=None):
            main()
        mock_logging.error.assert_called_with("Network error occurred: %s", "Network error")

    @patch('src.main.json.load')
    @patch('src.main.open')
    @patch('src.main.logging')
    def test_missing_config_file(self, mock_logging, mock_open, mock_json_load):
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            main()
        mock_logging.error.assert_called_with("Configuration file not found.")

    @patch('src.main.WeatherService')
    @patch('src.main.logging')
    def test_invalid_api_key(self, mock_logging, mock_WeatherService):
        mock_config = {
            'API_KEY': 'invalid_api_key',
            'LOCATIONS': ['Delhi'],
            'INTERVAL': 300,
            'DURATION': 600
        }
        with patch('src.main.json.load', return_value=mock_config):
            mock_weather_service = MagicMock()
            mock_WeatherService.return_value = mock_weather_service
            mock_weather_service.fetch_weather_data.side_effect = Exception("API authentication failed")
            with self.assertRaises(Exception):
                main()
        mock_logging.error.assert_called_with("API authentication failed.")

    @patch('src.main.Visualization')
    @patch('src.main.logging')
    def test_visualization_failure(self, mock_logging, mock_Visualization):
        mock_config = {
            'API_KEY': 'mock_api_key',
            'LOCATIONS': ['Delhi'],
            'INTERVAL': 300,
            'DURATION': 600
        }
        with patch('src.main.json.load', return_value=mock_config):
            mock_visualization = MagicMock()
            mock_Visualization.return_value = mock_visualization
            mock_visualization.plot.side_effect = Exception("Visualization failed")
            with self.assertRaises(Exception):
                main()
        mock_logging.error.assert_called_with("Visualization failed")

    @patch('src.main.logging')
    def test_graceful_shutdown(self, mock_logging):
        with patch('src.main.time.sleep', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                main()
        mock_logging.info.assert_called_with("Shutting down gracefully.")

    @patch('src.main.AlertService')
    @patch('src.main.WeatherService')
    def test_alert_service_triggering_alerts(self, mock_WeatherService, mock_AlertService):
        mock_config = {
            'API_KEY': 'mock_api_key',
            'LOCATIONS': ['CityA'],
            'INTERVAL': 300,
            'DURATION': 600
        }
        with patch('src.main.json.load', return_value=mock_config):
            mock_weather_service = MagicMock()
            mock_WeatherService.return_value = mock_weather_service
            mock_weather_service.fetch_weather_data.return_value = {
                'CityA': {'main': {'temp': 320, 'humidity': 85}, 'wind': {'speed': 20}}
            }
            mock_alert_service = MagicMock()
            mock_AlertService.return_value = mock_alert_service
            mock_alert_service.check_alerts.return_value = ["Alert! CityA temperature exceeded 35°C."]
            main()
        mock_alert_service.check_alerts.assert_called_once()

if __name__ == '__main__':
    unittest.main()
