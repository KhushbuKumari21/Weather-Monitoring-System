import matplotlib.pyplot as plt
import numpy as np

class Visualization:
    def display_bar_chart(self, title, x_labels, y_values, ylabel, colors):
        plt.figure(figsize=(10, 5))
        plt.title(title)
        bar_width = 0.3
        x_indices = np.arange(len(x_labels))
        plt.bar(x_indices, y_values, width=bar_width, color=colors)
        plt.xticks(x_indices, x_labels)
        plt.ylabel(ylabel)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def display_summary(self, daily_summary):
        for day, summary in daily_summary.items():
            if self.validate_summary(summary):
                self.display_bar_chart(
                    title=f"Daily Weather Summary for {day}",
                    x_labels=['Avg Temp', 'Max Temp', 'Min Temp', 'Avg Humidity', 'Avg Wind Speed'],
                    y_values=[
                        summary['average_temp'],
                        summary['max_temp'],
                        summary['min_temp'],
                        summary.get('average_humidity', 0),
                        summary.get('average_wind_speed', 0)
                    ],
                    ylabel='Values',
                    colors=['blue', 'red', 'green', 'purple', 'orange']
                )
            else:
                print(f"Validation failed for summary on {day}: {summary}")

    def display_forecast_summary(self, forecast_summary):
        for forecast_day, locations in forecast_summary.items():
            for location, summary in locations.items():
                if self.validate_summary(summary, is_forecast=True):
                    self.display_bar_chart(
                        title=f"Forecast Summary for {location} on {forecast_day}",
                        x_labels=['Avg Temp', 'Avg Humidity', 'Avg Wind Speed'],
                        y_values=[
                            summary['average_temp'],
                            summary.get('average_humidity', 0),
                            summary.get('average_wind_speed', 0)
                        ],
                        ylabel='Values',
                        colors=['orange', 'purple', 'cyan']
                    )
                else:
                    print(f"Validation failed for forecast summary for {location} on {forecast_day}: {summary}")

    def validate_summary(self, summary, is_forecast=False):
        required_keys = ['average_temp']
        if is_forecast:
            required_keys += ['average_humidity', 'average_wind_speed']
        else:
            required_keys += ['max_temp', 'min_temp']
        return all(key in summary for key in required_keys)

    def run_batch_visualization(self, daily_summaries):
        for daily_summary in daily_summaries:
            self.display_summary(daily_summary)

    def run_batch_forecast_visualization(self, forecast_summaries):
        for forecast_summary in forecast_summaries:
            self.display_forecast_summary(forecast_summary)
