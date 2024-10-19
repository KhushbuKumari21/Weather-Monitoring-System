import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherAggregator:
    def __init__(self):
        self.daily_data = {}
        self.current_date = None

    def collect_weather_data(self, weather_data):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        if self.current_date is None:
            self.current_date = date_str

        if date_str != self.current_date:
            self.aggregate_daily_data()
            self.current_date = date_str
            self.daily_data.clear()

        for location, weather in weather_data.items():
            temp_k = weather.get('main', {}).get('temp')
            if temp_k is not None:
                temp_c = self.kelvin_to_celsius(temp_k)
                self.daily_data.setdefault(location, []).append(temp_c)

    def aggregate_daily_data(self):
        for location, temps in self.daily_data.items():
            if temps:
                avg_temp = sum(temps) / len(temps)
                max_temp = max(temps)
                min_temp = min(temps)

                daily_summary = {
                    'date': self.current_date,
                    'location': location,
                    'average_temperature': avg_temp,
                    'max_temperature': max_temp,
                    'min_temperature': min_temp,
                }
                self.store_daily_summary(daily_summary)

    def store_daily_summary(self, summary):
        logging.info(f"Daily Summary: {summary}")

    def kelvin_to_celsius(self, kelvin):
        return kelvin - 273.15
