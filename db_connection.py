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
    except mysql.connector.Error as err:
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

def get_post(post_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
        SELECT p.*, u.username, u.display_name
        FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.id = %s AND p.visibility = 'public'
    """, (post_id,))
    result = cursor.fetchone()
    close_db_connection(cursor, conn)
    return result

def get_posts(limit, offset):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
        SELECT p.*, u.username, u.display_name
        FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.visibility = 'public' 
        ORDER BY p.created_at DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))
    result = cursor.fetchall()
    close_db_connection(cursor, conn)
    return result

def get_trending_posts(time_filter, limit):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute(f"""
        SELECT 
            p.id, 
            p.caption, 
            p.image_filename, 
            p.created_at,
            p.comment_count, 
            p.like_count, 
            u.username,
            u.display_name
        FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE {time_filter}
        ORDER BY (p.comment_count + p.like_count) DESC
        LIMIT %s
    """, (limit,))
    result = cursor.fetchall()
    close_db_connection(cursor, conn)
    return result

def create_post(user_id, caption, image_filename, category=None, visibility='public', tags=None):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
        INSERT INTO posts (user_id, caption, image_filename, category, visibility, tags)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, caption, image_filename, category, visibility, tags))
    conn.commit()
    post_id = cursor.lastrowid

    cursor.execute("""
        SELECT 
            id, 
            caption, 
            image_filename, 
            created_at,
            category, 
            visibility, 
            tags,
            like_count,
            comment_count,
            user_id
        FROM posts 
        WHERE id = %s
    """, (post_id,))
    new_post = cursor.fetchone()
    close_db_connection(cursor, conn)
    return new_post

def delete_post(post_id, user_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("DELETE FROM posts WHERE id = %s AND user_id = %s", (post_id, user_id))
    conn.commit()
    affected_rows = cursor.rowcount
    close_db_connection(cursor, conn)
    return affected_rows > 0