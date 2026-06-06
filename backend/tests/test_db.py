from backend.db.connection import get_db_connection

def test_connection():
    """Test Supabase database connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check current database
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        print(f"✅ Connected to database: {db[0]}")
        
        # Check Supabase version (optional)
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL version: {version[0][:50]}...")
        
        # Check connection time (optional)
        cursor.execute("SELECT NOW();")
        now = cursor.fetchone()
        print(f"✅ Server time: {now[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()