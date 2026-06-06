import hashlib
import secrets
from datetime import datetime, timedelta
from db.connection import get_db_connection

def _hash_code(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def create_otp(user_id: int) -> str:
    """Generate a 6-digit OTP, store its hash, return the raw code."""
    raw_code = str(secrets.randbelow(900_000) + 100_000)
    code_hash = _hash_code(raw_code)
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    conn = get_db_connection()
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
                        """, (user_id, code_hash, expires_at))
                    

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    return raw_code

def verify_otp(raw_code: str, new_password_hash: str) -> str:
    """Mark token used and update the user's password atomically."""
    code_hash = _hash_code(raw_code)

    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT t.id, t.user_id
                FROM password_reset_tokens t
                WHERE t.token_hash = %s
                  AND t.used = FALSE
                  AND t.expires_at > NOW()
            """, (code_hash,))
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