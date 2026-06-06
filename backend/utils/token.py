import jwt
from datetime import datetime, timedelta, timezone
from backend.config import Config

def generate_access_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def generate_refresh_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def decode_token(token, expected_type="access"):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != expected_type:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
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
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")