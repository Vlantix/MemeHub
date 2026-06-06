from backend.db.connection import get_db_connection, get_dict_cursor, close_db_connection

def get_user_profile_by_id(user_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
        SELECT id, display_name, username, email, bio,
               profile_photo_url, cover_photo_url
        FROM users
        WHERE id = %s
    """, (user_id,))
    result = cursor.fetchone()
    close_db_connection(cursor, conn)
    return result

def get_user_posts(user_id, limit, offset=0):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
        SELECT id, caption, image_filename, created_at, category, visibility, tags, like_count, comment_count
        FROM posts 
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, (user_id, limit, offset))
    result = cursor.fetchall()
    close_db_connection(cursor, conn)
    return result

def get_total_likes(post_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("SELECT like_count FROM posts WHERE id = %s", (post_id,))
    result = cursor.fetchone()
    close_db_connection(cursor, conn)
    return result['like_count'] if result else 0

def get_total_posts(user_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("SELECT COUNT(*) as count FROM posts WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    close_db_connection(cursor, conn)
    return result['count'] if result else 0

def update_user_profile(user_id, display_name=None, bio=None):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
        UPDATE users 
        SET display_name = COALESCE(%s, display_name), 
            bio = COALESCE(%s, bio) 
        WHERE id = %s
    """, (display_name, bio, user_id))
    conn.commit()
    affected_rows = cursor.rowcount
    close_db_connection(cursor, conn)
    return affected_rows > 0

def update_profile_photo(user_id, url, filename):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    try:
        cursor.execute("""
            UPDATE users
            SET profile_photo_url = %s,
                profile_photo_filename = %s
            WHERE id = %s
        """, (url, filename, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        close_db_connection(cursor, conn)

def update_cover_photo(user_id, url, filename):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    try:
        cursor.execute("""
            UPDATE users
            SET cover_photo_url = %s,
                cover_photo_filename = %s
            WHERE id = %s
        """, (url, filename, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        close_db_connection(cursor, conn)

def get_user_photo_filenames(user_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
        SELECT profile_photo_filename, cover_photo_filename
        FROM users WHERE id = %s
    """, (user_id,))
    result = cursor.fetchone()
    close_db_connection(cursor, conn)
    return result