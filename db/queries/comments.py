from db.connection import get_db_connection, get_dict_cursor, close_db_connection

def add_comment(user_id, post_id, content):

    if not content or not content.strip():
        print("Error: Comment content cannot be empty")
        return None

    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("""INSERT INTO comments (user_id, post_id, content)
                       VALUES (%s, %s, %s) RETURNING id""", (user_id, post_id, content))
        comment_id = cursor.fetchone()['id']

        cursor.execute("UPDATE posts SET comment_count = comment_count + 1 WHERE id = %s", (post_id,))
        
        conn.commit()
        
        cursor.execute("""SELECT c.id, c.content, c.created_at, u.display_name
                       FROM comments c
                       JOIN users u ON c.user_id = u.id
                       WHERE c.id = %s""", (comment_id,))
        result = cursor.fetchone()
        return result
    
    except Exception as e:
        conn.rollback()
        print(f"Error adding comment: {e}")
        return None
    
    finally:
        close_db_connection(cursor, conn)

def get_comments(post_id, limit, offset, user_id=None):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("""
            SELECT c.id, c.content, c.created_at, c.user_id,
                   u.username, u.display_name
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = %s
            ORDER BY c.created_at DESC
            LIMIT %s OFFSET %s
        """, (post_id, limit, offset))
        
        results = cursor.fetchall()
        
        if user_id:
            for comment in results:
                comment['is_owner'] = (comment['user_id'] == user_id)
        
        return results
    finally:
        close_db_connection(cursor, conn)

def delete_comment(comment_id, user_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("SELECT post_id FROM comments WHERE id = %s AND user_id = %s", (comment_id, user_id))
        result = cursor.fetchone()
        
        if not result:
            return False
        
        post_id = result['post_id']
        
        cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        
        cursor.execute("UPDATE posts SET comment_count = comment_count - 1 WHERE id = %s", (post_id,))
        
        conn.commit()
        return True
    
    except Exception as e:
        conn.rollback()
        print(f"Error deleting comment: {e}")
        return False

    finally:
        close_db_connection(cursor, conn)

def get_comment_count(post_id):
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("SELECT comment_count FROM posts WHERE id = %s", (post_id,))
        result = cursor.fetchone()
        
        return result['comment_count'] if result else 0

    finally:
        close_db_connection(cursor, conn)

def update_comment(comment_id, user_id, content):
    if not content or not content.strip():
        print("Error: Comment content cannot be empty")
        return False

    conn = get_db_connection()
    cursor = get_dict_cursor(conn)

    try:
        cursor.execute("UPDATE comments SET content = %s WHERE id = %s AND user_id = %s", (content, comment_id, user_id))
        conn.commit()
        return cursor.rowcount > 0 
    
    except Exception as e:
        conn.rollback()
        print(f"Error updating comment: {e}")
        return False
    
    finally:
        close_db_connection(cursor, conn)
    