from backend.db.connection import get_db_connection, get_dict_cursor, close_db_connection

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

def get_trending_posts(interval, limit):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
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
        WHERE p.created_at >= NOW() - %s::interval
        ORDER BY (p.comment_count + p.like_count) DESC
        LIMIT %s
    """, (interval, limit))
    result = cursor.fetchall()
    close_db_connection(cursor, conn)
    return result

def create_post(user_id, caption, image_filename, image_url=None, category=None, visibility='public', tags=None):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute("""
        INSERT INTO posts (user_id, caption, image_filename, image_url, category, visibility, tags)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
    """, (user_id, caption, image_filename, image_url, category, visibility, tags))
    post_id = cursor.fetchone()['id']
    conn.commit()

    cursor.execute("""
        SELECT 
            id, 
            caption, 
            image_filename,
            image_url,
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