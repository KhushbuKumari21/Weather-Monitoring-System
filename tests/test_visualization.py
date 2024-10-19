import unittest
from unittest.mock import patch
from src.visualization import Visualization  

class TestVisualization(unittest.TestCase):
    
    @patch('src.visualization.plt.figure')
    @patch('src.visualization.plt.bar')
    @patch('src.visualization.plt.show')
    def test_display_summary_valid_data(self, mock_show, mock_bar, mock_figure):
        visualization = Visualization()
        daily_summary = {
            '2024-10-19': {
                'average_temp': 28,
                'max_temp': 30,
                'min_temp': 26,
                'average_humidity': 65,
                'average_wind_speed': 10
            }
        }
        visualization.display_summary(daily_summary)
        mock_figure.assert_called()
        mock_bar.assert_called()
        mock_show.assert_called()

    @patch('builtins.print')
    def test_display_summary_invalid_data(self, mock_print):
        visualization = Visualization()
        daily_summary = {
            '2024-10-19': {
                'average_temp': 28,
                'average_humidity': 65,
            }
        }
        visualization.display_summary(daily_summary)
        mock_print.assert_called_with("Validation failed for summary on 2024-10-19: {'average_temp': 28, 'average_humidity': 65}")

    @patch('builtins.print')
    def test_display_summary_empty_data(self, mock_print):
        visualization = Visualization()
        daily_summary = {}
        visualization.display_summary(daily_summary)
        mock_print.assert_not_called()

    @patch('src.visualization.plt.figure')
    @patch('src.visualization.plt.bar')
    @patch('src.visualization.plt.show')
    def test_display_forecast_summary_valid_data(self, mock_show, mock_bar, mock_figure):
        visualization = Visualization()
        forecast_summary = {
            '2024-10-19': {
                'Delhi': {
                    'average_temp': 28,
                    'average_humidity': 65,
                    'average_wind_speed': 10
                }
            }
        }
        visualization.display_forecast_summary(forecast_summary)
        mock_figure.assert_called()
        mock_bar.assert_called()
        mock_show.assert_called()

    @patch('builtins.print')
    def test_display_forecast_summary_invalid_data(self, mock_print):
        visualization = Visualization()
        forecast_summary = {
            '2024-10-19': {
                'Delhi': {
                    'average_temp': 28,
                }
            }
        }
        visualization.display_forecast_summary(forecast_summary)
        mock_print.assert_called_with("Validation failed for forecast summary for Delhi on 2024-10-19: {'average_temp': 28}")

if __name__ == '__main__':
    unittest.main()
