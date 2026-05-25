from db.connection import get_db_connection, get_dict_cursor, close_db_connection 

def add_like(user_id, post_id):
    try:
        conn = get_db_connection()
        cursor = get_dict_cursor(conn)
        
        cursor.execute("SELECT id FROM likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
        existing_like = cursor.fetchone()
        
        if existing_like:
            close_db_connection(cursor, conn)
            return False  
        
        cursor.execute("INSERT INTO likes (user_id, post_id) VALUES (%s, %s)", (user_id, post_id))
        
        cursor.execute("UPDATE posts SET like_count = like_count + 1 WHERE id = %s", (post_id,))
        
        conn.commit()
        return True

    finally:
        close_db_connection(cursor, conn)

def remove_like(user_id, post_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try: 
        cursor.execute("SELECT id FROM likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
        existing_like = cursor.fetchone()
        
        if not existing_like:
            return False  
        
        cursor.execute("DELETE FROM likes WHERE id = %s", (existing_like['id'],))
        
        cursor.execute("UPDATE posts SET like_count = like_count - 1 WHERE id = %s", (post_id,))
        
        conn.commit()
        return True

    finally:
        close_db_connection(cursor, conn)

def check_user_liked(user_id, post_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("SELECT id FROM likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
        result = cursor.fetchone()
        
        return result is not None

    finally:
        close_db_connection(cursor, conn)

def get_post_like_count(post_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("SELECT like_count FROM posts WHERE id = %s", (post_id,))
        result = cursor.fetchone()
        
        return result['like_count'] if result else 0

    finally:
        close_db_connection(cursor, conn)

def get_users_who_liked(post_id, limit):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("""
            SELECT u.display_name 
            FROM likes l
            JOIN users u ON l.user_id = u.id 
            WHERE l.post_id = %s
            LIMIT %s
        """, (post_id, limit))
        results = cursor.fetchall()
        return results
    finally:
        close_db_connection(cursor, conn)