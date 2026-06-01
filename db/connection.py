import psycopg2
import psycopg2.extras
from config import Config

def get_db_connection():
    try:
        connection = psycopg2.connect(Config.DATABASE_URL)
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return None
    
    return connection

def get_dict_cursor(connection):
    """Returns a dictionary cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def close_db_connection(cursor, conn):
    cursor.close()
    conn.close()