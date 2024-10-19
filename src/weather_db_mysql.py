import mysql.connector
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='khushbu123',
            database='weather_db'
        )
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to the database: {e}")
        return None

def create_tables():
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS daily_weather_summary (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            location VARCHAR(255),
            avg_temp FLOAT,
            max_temp FLOAT,
            min_temp FLOAT,
            dominant_condition VARCHAR(255),
            UNIQUE KEY unique_date_location (date, location)
        )''')
        conn.commit()  # Explicitly call commit
        logging.info("Table 'daily_weather_summary' created or already exists.")
    except mysql.connector.Error as e:
        logging.error(f"Error creating table: {e}")
    finally:
        cursor.close()  # Always close the cursor
        conn.close()    # Close the connection

def insert_summaries(data):
    if not data:  # Check if the data list is empty
        logging.info("No data to insert.")
        return

    conn = create_connection()
    if conn is None:
        logging.error("Database connection failed. Cannot proceed with data insertion.")
        return

    try:
        with conn:
            cursor = conn.cursor()
            formatted_data = [
                (str(date), location, avg_temp, max_temp, min_temp, dominant_condition)
                for (date, location, avg_temp, max_temp, min_temp, dominant_condition) in data
            ]
            cursor.executemany('''
                INSERT INTO daily_weather_summary (date, location, avg_temp, max_temp, min_temp, dominant_condition)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    avg_temp = VALUES(avg_temp),
                    max_temp = VALUES(max_temp),
                    min_temp = VALUES(min_temp),
                    dominant_condition = VALUES(dominant_condition);
            ''', formatted_data)
            conn.commit()
            logging.info("Inserted or updated summary data successfully.")
    except mysql.connector.Error as e:
        logging.error(f"Failed to insert summaries into daily_weather_summary: {e}")


def get_average_temperature(location):
    conn = create_connection()
    if conn is None:
        return None

    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT AVG(avg_temp) FROM daily_weather_summary WHERE location = %s
            ''', (location,))
            avg_temp = cursor.fetchone()
            return avg_temp[0] if avg_temp else None
        except mysql.connector.Error as e:
            logging.error(f"Failed to retrieve average temperature: {e}")
            return None

if __name__ == "__main__":
    create_tables()
    weather_data = [
        ('2024-10-17', 'New York', 65.0, 70.0, 60.0, 'Sunny'),
        ('2024-10-17', 'Los Angeles', 75.0, 80.0, 70.0, 'Clear'),
        ('2024-10-17', 'Chicago', 55.0, 60.0, 50.0, 'Cloudy'),
        ('2024-10-20', 'Mumbai', 28.5, 30.0, 25.0, 'Clear'),
        ('2024-10-20', 'Delhi', 22.0, 24.0, 20.0, 'Cloudy'),
        ('2024-10-20', 'Kolkata', 30.0, 32.0, 28.0, 'Rainy')
    ]
    insert_summaries(weather_data)
