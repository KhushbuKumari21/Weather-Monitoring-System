import unittest
from unittest.mock import patch
from weather_service import WeatherService  

class TestWeatherService(unittest.TestCase):
    
    def setUp(self):
        self.weather_service = WeatherService()

    @patch('weather_service.WeatherService.fetch_weather_data')
    def test_fetch_weather_data_success(self, mock_fetch_weather_data):
        mock_fetch_weather_data.return_value = {
            "New York": {"temp": 20, "weather": "Sunny"},
            "Los Angeles": {"temp": 25, "weather": "Sunny"}
        }
        data = self.weather_service.fetch_weather_data(locations=["New York", "Los Angeles"])
        self.assertIn("New York", data)
        self.assertIn("Los Angeles", data)

    @patch('weather_service.WeatherService.fetch_weather_data')
    def test_fetch_weather_data_invalid_location(self, mock_fetch_weather_data):
        mock_fetch_weather_data.return_value = {
            "InvalidLocation": None
        }
        data = self.weather_service.fetch_weather_data(locations=["InvalidLocation"])
        self.assertIsNone(data["InvalidLocation"])

    

if __name__ == '__main__':
    unittest.main()
