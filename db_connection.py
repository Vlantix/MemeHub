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

def close_db_connection(cursor, conn):
    cursor.close()
    conn.close()

def create_account(display_name, username, email, password_hash):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""INSERT INTO users(
                   display_name,
                   username,
                   email,
                   password_hash
                   ) VALUES (%s, %s, %s, %s)""", 
                   (display_name, username, email, password_hash))
    conn.commit()
    close_db_connection(cursor, conn)

def get_username(username):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    close_db_connection(cursor, conn)
    return result

def get_email(email):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    close_db_connection(cursor, conn)
    return result