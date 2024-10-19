import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import mysql

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.weather_db_mysql import create_tables, insert_summaries, get_average_temperature, create_connection

class TestDatabaseOperations(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_create_tables(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        create_tables()

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_insert_summaries(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        data = [
            ('2024-10-20', 'Mumbai', 28.5, 30.0, 25.0, 'Clear'),
            ('2024-10-20', 'Delhi', 22.0, 24.0, 20.0, 'Cloudy')
        ]
        insert_summaries(data)

        self.assertEqual(mock_cursor.executemany.call_count, 1)
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_insert_empty_data(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        data = []
        insert_summaries(data)

        mock_cursor.executemany.assert_not_called()
        mock_conn.commit.assert_not_called()

    @patch('mysql.connector.connect')
    def test_get_average_temperature(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (75.0,)
        avg_temp = get_average_temperature('Mumbai')
        self.assertEqual(avg_temp, 75.0)

        mock_cursor.fetchone.return_value = None
        avg_temp = get_average_temperature('Nonexistent Location')
        self.assertIsNone(avg_temp)

    @patch('mysql.connector.connect')
    def test_create_connection_failure(self, mock_connect):
        mock_connect.side_effect = mysql.connector.Error("Connection failed")
        conn = create_connection()
        self.assertIsNone(conn)

if __name__ == '__main__':
    unittest.main()
