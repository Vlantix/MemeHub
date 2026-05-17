from db.connection import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    db = cursor.fetchone()
    print(f"✅ Connected to database: {db[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")