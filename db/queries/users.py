from db.connection import get_db_connection, get_dict_cursor, close_db_connection

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
    user_id = cursor.lastrowid
    close_db_connection(cursor, conn)
    return user_id

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