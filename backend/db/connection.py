import psycopg2
import psycopg2.extras
from backend.config import Config

def get_db_connection():
    if not Config.DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    print(f"Attempting connection to: {Config.DATABASE_URL}")
    try:
        connection = psycopg2.connect(Config.DATABASE_URL)
    except Exception as err:
        print(f"Error: {err}")
        raise
    
    return connection

def get_dict_cursor(connection):
    """Returns a dictionary cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def close_db_connection(cursor, conn):
    cursor.close()
    conn.close()