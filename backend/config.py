import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG", "FALSE").upper() == "TRUE"

    DATABASE_URL = os.getenv("DATABASE_URL")

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

    RESEND_API_KEY = None
    RESEND_SENDER_EMAIL = None