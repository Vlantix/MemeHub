import mysql.connector
from config import Config

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host = Config.DB_HOST,
            user = Config.DB_USER,
            password = Config.DB_PASSWORD,
            database = Config.DB_NAME
        )
    except mysql.connector.error as err:
        print(f"Error: {err}")
        return None
    
    return connection

def get_dict_cursor(connection):
    """Returns a dictionary cursor"""
    return connection.cursor(dictionary=True)