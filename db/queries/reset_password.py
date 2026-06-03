import hashlib
import secrets
from datetime import datetime, timedelta
from db.connection import get_db_connection

def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def create_reset_token(user_id: int) -> str:
    """Generate a token, store its hash, return the raw token."""
    raw_token = secrets.token_urlsafe(32)
    token_hash = _hash_token(raw_token)
    expires_at = datetime.utcnow() + timedelta(hours=1)

    conn = get_db_connection
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        UPDATE password_reset_tokens
                        SET used = TRUE
                        WHERE user_id = %s AND used = FALSE
                        """, (user_id,))
            
            cur.execute("""
                        INSERT INTO password_reset_tokens(
                        user_id, token_hash, expires_at)
                        VALUES (%s, %s, %s)
                        """, (user_id, token_hash, expires_at))
    except Exception:
        conn.roolback()
        raise
    finally:
        conn.close()

    return raw_token

def consume_reset_token(raw_token: str, new_password_hash: str) -> str:
    """Mark token used and update the user's password atomically."""
    token_hash = _hash_token(raw_token)

    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT t.id, t.user_id
                FROM password_reset_tokens t
                WHERE t.token_hash = %s
                  AND t.used = FALSE
                  AND t.expires_at > NOW()
            """, (token_hash,))
            row = cur.fetchone()

            if not row:
                return False

            token_id, user_id = row

            cur.execute("""
                UPDATE password_reset_tokens SET used = TRUE WHERE id = %s
            """, (token_id,))

            cur.execute("""
                UPDATE users SET password_hash = %s WHERE id = %s
            """, (new_password_hash, user_id))

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()