# backend/config/db.py
# Database connection configuration using mysql-connector-python

import mysql.connector
from mysql.connector import Error
import os

def get_db_connection():
    """
    Returns a MySQL database connection.
    Uses environment variables for credentials.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            database=os.getenv('DB_NAME', 'inventory_db'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            autocommit=True
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[DB ERROR] Could not connect to MySQL: {e}")
        return None

def close_connection(connection, cursor=None):
    """Safely close cursor and connection."""
    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"[DB ERROR] Error closing connection: {e}")
