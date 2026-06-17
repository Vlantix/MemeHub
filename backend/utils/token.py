import jwt
from datetime import datetime, timedelta, timezone
from config import Config
import logging

logger = logging.getLogger(__name__)

def generate_access_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "type": "access",
        "issued_at": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def generate_refresh_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "type": "refresh",
        "issued_at": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def decode_token(token, expected_type="access"):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

        if payload.get("type") != expected_type:
            return None
        
        exp = payload.get("exp")

        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            return None
        
        return payload
    
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        logger.error(f"Token decode error: {e}")
        return None
    
def generate_reset_session_token(user_id: int) -> str:
    """
    Short-lived token issued after OTP verification.
    Passed by the client to /auth/reset-password to authorize the password change.
    5-minute window — just long enough to fill the new-password form.
    """
    payload = {
        "user_id": user_id,
        "type": "password_reset",
        "issued_at": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")