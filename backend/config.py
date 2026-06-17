import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    RESEND_SENDER_EMAIL = os.getenv("RESEND_SENDER_EMAIL")
    DEBUG = os.getenv("DEBUG", "False").upper() == "TRUE"
    PORT = int(os.getenv("PORT", 10000))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1000 * 1000))

    @classmethod
    def validate(cls):
        """Check if all required environment variables are set"""
        required_vars = [
            'SECRET_KEY',
            'DATABASE_URL', 
            'SUPABASE_URL',
            'SUPABASE_KEY',
            'SUPABASE_BUCKET',
            'RESEND_API_KEY',
            'RESEND_SENDER_EMAIL'
        ]
        
        missing = []
        for var in required_vars:
            if not getattr(cls, var, None):
                missing.append(var)
        
        if missing:
            raise ValueError(
                f"Missing required environment variables:\n"
                f"   {', '.join(missing)}\n\n"
                f"Please set them in your .env file or environment."
            )
        
        if cls.SECRET_KEY == 'your-secret-key-here':
            print("WARNING: Using default SECRET_KEY. Change this in production!")
        
        print("All required environment variables are set.")
        return True