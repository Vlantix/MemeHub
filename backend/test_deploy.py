from config import Config
from db.connection import get_db_connection

print("🔍 Testing configuration...")
Config.validate()
print("✅ Config OK")

print("🔍 Testing database...")
conn = get_db_connection()
print("✅ Database OK")
conn.close()

print("🎉 All systems ready for deployment!")