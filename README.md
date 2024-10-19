
# Weather Monitoring System

## Objective
Develop a real-time data processing system to monitor weather conditions and provide summarized insights using rollups and aggregates.

## Features
- Continuous retrieval of weather data from the OpenWeatherMap API.
- Daily weather summaries with aggregates: average, max, min temperatures, and dominant weather conditions.
- User-configurable alerting thresholds for temperature.
- Visualization of daily weather summaries and forecast summaries.
- Support for additional weather parameters (humidity, wind speed).
- Forecast retrieval for predicted weather conditions.

## Dependencies
- Python 3.9+
- `requests` for API calls
- `matplotlib` for visualization
- `mysql-connector-python` for MySQL database connectivity
- `pandas` for data manipulation
## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/KhushbuKumari21/Weather-Monitoring-System.git
   cd weather-monitoring-system
2. Set up your environment:
   pip install -r requirements.txt
3. Replace your_api_key_here in main.py with your actual OpenWeatherMap API key.

4. Set up your MySQL database:
   Create a database named weather_db:
   CREATE DATABASE weather_db;
  
5. Run the database setup script:
   python src/weather_db_mysql.py
6. Run Application
   python main.py

   


 
## Running with Docker
1. Build the Docker image:
   docker build -t weather-monitor .

2. Run the application:
   docker run -d -p 5000:5000 weather-monitor

## Testing
  Step 1 : cd tests
  step 2 :$env:PYTHONPATH = ".."
  step 3 which Test file  you want test :
  python -m unittest test_visualization.py 
  python -m unittest test_alert_service.py
  python -m unittest test_weather_service.py
  python -m unittest test_main.py  
  python -m unittest test_aggregator.py    
  python -m unittest test_monitor.py 
  python -m unittest test_database.py
 
## What Works on Which File :
   # Main.py 
   1.Data Fetching:
     Retrieves current weather and forecast data from specified locations using the WeatherService class.
   2.Processing and Alerts:
     Processes the fetched weather data and checks for alerts using the AlertService class, logging any triggered alerts.
   3.Visualization:
     Displays daily weather summaries and forecasts through the Visualization class.
   4.Error Handling:
     Manages network errors and JSON parsing issues, ensuring reliable operation and logging any errors encountered.
   5.Duration Control:
     Allows monitoring to run for a defined duration, automatically terminating after the specified period.

 # alert_service.py
   1.Threshold Management:
      Initializes default thresholds for temperature, humidity, and wind speed.
      Allows setting custom thresholds for specific weather conditions.
   2.Temperature Conversion:
      Converts temperature from Kelvin to Celsius and Fahrenheit using dedicated methods (kelvin_to_celsius and kelvin_to_fahrenheit).
   3.Alert Checking:
      Monitors weather data for specified locations, checking if any conditions exceed defined thresholds:
        a.Temperature Alerts: Generates alerts if the temperature exceeds the set threshold and tracks consecutive exceedances.
        b.Humidity Alerts: Generates alerts if humidity exceeds the defined threshold.
        c.Wind Speed Alerts: Generates alerts if wind speed exceeds the set threshold.
      Logs errors when required data is missing, ensuring robustness in data processing.
   4.Alert Sending:
      Provides functionality to send alerts through the send_alert method, logging the message being sent.
   5.Alert Evaluation:
      Evaluates and processes alerts based on the current weather data, invoking both the alert checking and sending functions in one method (evaluate_alerts).
# visualation.py
   1. Bar Chart Display:
      (a)display_bar_chart:
        Creates and displays a bar chart using Matplotlib.
        Accepts parameters for the chart title, x-axis labels, y-values, y-axis label, and colors for the bars.
        Configures the chart layout, including size, title, labels, and grid lines for better readability.
   2. Daily Summary Visualization:
      (a)display_summary:
         Iterates over daily weather summaries and validates each summary.
         If valid, calls display_bar_chart to visualize average, maximum, and minimum temperatures, average humidity, and average wind speed.
         If validation fails, it prints an error message with the day's summary.
   3. Forecast Summary Visualization:
      (a)display_forecast_summary:
        Iterates over forecast summaries for different locations on specified days.
        Validates each summary before visualization.
        If valid, visualizes average temperature, average humidity, and average wind speed using display_bar_chart.
        Prints an error message for any invalid summaries.
   4. Summary Validation:
      (a)validate_summary:
         Checks if all required keys are present in the summary dictionary.
         Customizes required keys based on whether the summary is for a daily report or a forecast.
   5.Batch Visualization:
      (a)run_batch_visualization:
         Accepts a list of daily summaries and displays each one sequentially.
      (b)run_batch_forecast_visualization:
        Accepts a list of forecast summaries and displays each one sequentially.
# weather_aggregator.py 
   1.Initialization:
      (a) __init__:
         Initializes an empty dictionary to hold daily weather data (daily_data).
         Sets current_date to None.
   2.Weather Data Collection:
     (a)collect_weather_data:
        Fetches the current date and formats it as a string (YYYY-MM-DD).
        Checks if current_date is set; if not, initializes it with the current date.
        If the date has changed since the last collection, it aggregates the previous day's data and clears daily_data.
        Iterates over the provided weather data, extracting temperature in Kelvin, converting it to Celsius, and appending it to the list of temperatures for each location.
   3.Daily Data Aggregation:
      (a)aggregate_daily_data:
       Calculates daily summaries for each location from the collected temperature data.
       Computes average, maximum, and minimum temperatures for the day.
       Creates a summary dictionary containing the date, location, average temperature, maximum temperature, and minimum temperature.
       Calls store_daily_summary to log the daily summary.
   4.Daily Summary Storage:
      (a)store_daily_summary:
         Logs the daily summary information using the logging module at the INFO level.
   5.Temperature Conversion:
      (a)kelvin_to_celsius:
        Converts temperature from Kelvin to Celsius by subtracting 273.15.
# weather_db_mysql.py
   1.Initialization:
     Accepts an API key and a list of locations.
     Initializes dictionaries to store daily and forecast summaries.
   2.Fetching Weather Data:
     Uses the OpenWeather API to fetch current weather and forecast data.
     Implements a retry mechanism for handling request failures.
   3.Data Processing:
     Processes current weather data to calculate temperature, humidity, wind speed, and weather conditions.
    Groups daily weather data by date and location.
   4.Logging:
    Uses the logging module to log successful and failed data fetches and processing errors.
# Database Management
   1.Creating Connection:
     Establishes a connection to a MySQL database (weather_db) using provided credentials.
   2.Creating Tables:
     Defines a table (daily_weather_summary) for storing daily weather summaries.
     Ensures that the table is created only if it doesn't already exist.
   3.Inserting Data:
     Inserts or updates weather summaries using the insert_summaries function.
     Utilizes ON DUPLICATE KEY UPDATE to handle existing entries.
   4.Retrieving Data:
     Implements a function (get_average_temperature) to calculate and return the average temperature for a specified location.
# weather_monitor.py
   1.Argument Parsing:
     Uses argparse to handle command-line arguments for locations to monitor and a temperature threshold.
     locations: List of locations (required).
     threshold: Temperature threshold for alerts (default is 35°C).
   2.Temperature Alert Checking:
     check_temperature_alert(weather_data, threshold): This function iterates through fetched weather data and checks if the temperature exceeds the specified threshold.
     Alerts are generated for locations where the temperature is above the threshold.
   3.Testing:
     test_temperature_alerts(): A unit test function that verifies the alert mechanism using predefined test data. It checks if the function correctly identifies locations exceeding the temperature threshold.
   4.Main Execution Flow:
     Parses command-line arguments to get the list of locations and threshold.
     Instantiates a WeatherService object to fetch weather data using an API key.
     For each location, it fetches weather data and populates a dictionary.
     Calls the alert checking function and prints any alerts to the console
# weather_service.py
   1.Initialization:

      (a)The __init__ method initializes the service with an API key and a list of locations.
         It also sets up dictionaries for storing daily and forecast summaries.
   2.Fetching Weather Data:
      (a)fetch_weather_data:
         Uses the OpenWeatherMap API to get current weather data for each specified location.
         Retries the request up to 3 times with a 2-second wait in case of failure (using the tenacity library).
         Logs success or error messages based on the outcome.
   3.Fetching Forecast Data:
      (a)fetch_forecast_data:
         Retrieves forecast data for each location from the OpenWeatherMap API.
         Similar error handling and logging as in fetch_weather_data.
   4.Logging Functions:
     (a)log_success and log_error:
        Helper methods to log successful fetches and errors with appropriate messages.
   5.Processing Weather Data:
    (a)process_weather_data:
      Extracts relevant weather information (temperature, humidity, wind speed, weather description) and populates the daily_summary.
      Checks for missing data and logs errors if any expected information is not present.
   6.Extracting Weather Summary:
    (a)extract_weather_summary:
       Processes individual weather entries, organizing data by timestamp.
      Updates daily summary statistics for temperature, humidity, wind speed, and weather conditions.
   7.Updating Daily Summary:
     (a)update_daily_summary:
        Computes average, maximum, minimum temperatures, and other relevant statistics based on the collected data for a specific date.
   8.Processing Forecast Data:
     (a)process_forecast_data:
        Clears previous forecast summaries and processes the new forecast data for each location.
   9.Extracting Forecast Summary:
     (a)extract_forecast_summary:
        Similar to extract_weather_summary, but works on forecast entries over a period.
        Organizes forecast data by date and location.
   10.Updating Forecast Summary:
     (a)update_forecast_summary:
        Inserts forecast summaries into a MySQL database for today’s date using the insert_summaries function from weather_db_mysql.
    
