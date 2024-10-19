import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.visualization import Visualization



class TestVisualization(unittest.TestCase):
    def setUp(self):
        self.visualization = Visualization()

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.bar')
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.grid')
    @patch('matplotlib.pyplot.xticks')
    @patch('matplotlib.pyplot.tight_layout')
    def test_display_bar_chart(self, mock_tight_layout, mock_xticks, mock_grid, mock_ylabel, mock_title, mock_figure, mock_bar, mock_show):
        self.visualization.display_bar_chart("Test Chart", ["A", "B"], [1, 2], "Y-Axis", ["blue", "red"])
        mock_figure.assert_called_once()
        mock_title.assert_called_once_with("Test Chart")
        mock_ylabel.assert_called_once_with("Y-Axis")
        mock_bar.assert_called_once()
        mock_show.assert_called_once()

    def test_validate_summary(self):
        valid_summary = {'average_temp': 25, 'max_temp': 30, 'min_temp': 20}
        invalid_summary = {'average_temp': 25}
        self.assertTrue(self.visualization.validate_summary(valid_summary))
        self.assertFalse(self.visualization.validate_summary(invalid_summary))

    def test_display_summary_valid_data(self):
        with patch('builtins.print') as mock_print:
            daily_summary = {
                '2024-10-19': {
                    'average_temp': 28,
                    'max_temp': 32,
                    'min_temp': 24,
                    'average_humidity': 65,
                    'average_wind_speed': 10
                }
            }
            self.visualization.display_summary(daily_summary)
            mock_print.assert_not_called()  # No validation failures, so print should not be called

    def test_display_summary_invalid_data(self):
        with patch('builtins.print') as mock_print:
            daily_summary = {
                '2024-10-19': {
                    'average_temp': 28,
                    # Missing max_temp and min_temp
                }
            }
            self.visualization.display_summary(daily_summary)
            mock_print.assert_called_once_with("Validation failed for summary on 2024-10-19: missing keys ['max_temp', 'min_temp']")

    def test_display_forecast_summary_valid_data(self):
        with patch('builtins.print') as mock_print:
            forecast_summary = {
                '2024-10-19': {
                    'Delhi': {
                        'average_temp': 30,
                        'average_humidity': 70,
                        'average_wind_speed': 15
                    }
                }
            }
            self.visualization.display_forecast_summary(forecast_summary)
            mock_print.assert_not_called()  # No validation failures

    def test_display_forecast_summary_invalid_data(self):
        with patch('builtins.print') as mock_print:
            forecast_summary = {
                '2024-10-19': {
                    'Delhi': {
                        'average_temp': 30,
                        # Missing average_humidity and average_wind_speed
                    }
                }
            }
            self.visualization.display_forecast_summary(forecast_summary)
            mock_print.assert_called_once_with("Validation failed for forecast summary for Delhi on 2024-10-19: missing keys ['average_humidity', 'average_wind_speed']")

if __name__ == '__main__':
    unittest.main()
