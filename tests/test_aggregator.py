import unittest
from unittest.mock import patch
from datetime import datetime
import logging
import os
import sys

# Ensure the src directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.weather_aggregator import WeatherAggregator

from src.weather_aggregator import WeatherAggregator
class TestWeatherAggregator(unittest.TestCase):
    def setUp(self):
        self.aggregator = WeatherAggregator()

    @patch('logging.info')
    def test_collect_weather_data(self, mock_logging):
        weather_data = {
            'New York': {'main': {'temp': 285.15}},
            'Los Angeles': {'main': {'temp': 295.15}},
            'Chicago': {'main': {'temp': 270.15}},
        }
        self.aggregator.collect_weather_data(weather_data)
        self.aggregator.aggregate_daily_data()
        self.assertTrue(mock_logging.called)
        self.assertIn('Daily Summary:', mock_logging.call_args[0][0])

    @patch('logging.info')
    def test_aggregate_daily_data(self, mock_logging):
        self.aggregator.collect_weather_data({
            'New York': {'main': {'temp': 285.15}},
            'Los Angeles': {'main': {'temp': 295.15}},
            'Chicago': {'main': {'temp': 270.15}},
        })
        self.aggregator.aggregate_daily_data()
        self.assertTrue(mock_logging.called)
        self.assertIn('Daily Summary:', mock_logging.call_args[0][0])

    @patch('logging.info')
    def test_empty_weather_data(self, mock_logging):
        self.aggregator.collect_weather_data({})
        self.aggregator.aggregate_daily_data()
        self.assertFalse(mock_logging.called)

    def test_kelvin_to_celsius_conversion(self):
        temp_k = 300.15
        expected_temp_c = 27.0
        converted_temp = self.aggregator.kelvin_to_celsius(temp_k)
        self.assertAlmostEqual(converted_temp, expected_temp_c)

    @patch('logging.info')
    def test_multiple_calls_on_different_days(self, mock_logging):
        weather_data = {
            'New York': {'main': {'temp': 285.15}},
            'Los Angeles': {'main': {'temp': 295.15}},
        }
        self.aggregator.collect_weather_data(weather_data)
        self.aggregator.aggregate_daily_data()

        # Simulate data collection on the next day
        self.aggregator.current_date = (datetime.now().strftime("%Y-%m-%d"))
        weather_data_next_day = {
            'New York': {'main': {'temp': 290.15}},
            'Los Angeles': {'main': {'temp': 300.15}},
        }
        self.aggregator.collect_weather_data(weather_data_next_day)
        self.aggregator.aggregate_daily_data()

        self.assertTrue(mock_logging.called)
        self.assertIn('Daily Summary:', mock_logging.call_args_list[-1][0][0])

if __name__ == '__main__':
    unittest.main()
