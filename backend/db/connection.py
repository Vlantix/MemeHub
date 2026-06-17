import psycopg2
import psycopg2.extras
from config import Config
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    if not Config.DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    try:
        connection = psycopg2.connect(Config.DATABASE_URL)
        return connection
    except Exception as err:
        logger.error(f"Database connection failed: {err}")
        raise

def validate_schema():
    """Check if all required tables exist"""
    conn = get_db_connection()
    cursor = get_dict_cursor(conn)
    
    required_tables = ['users', 'posts', 'comments', 'likes', 'password_reset_tokens']
    missing_tables = []

    for table in required_tables:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s 
                AND table_schema = 'public'
            )
        """, (table,))

        result = cursor.fetchone()
        exists = result['exists'] if result else False

        if not exists:
            missing_tables.append(table)

    close_db_connection(cursor, conn)

    if missing_tables:
        RuntimeError(f"Missing database tables: {', '.join(missing_tables)}")
    
    logger.info("✅ Database schema validation passed")
    return True


def get_dict_cursor(connection):
    """Returns a dictionary cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def close_db_connection(cursor, conn):
    cursor.close()
    conn.close()