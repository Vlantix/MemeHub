import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")
SENDER = os.getenv("RESEND_SENDER_EMAIL")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def send_password_reset(to_email, raw_token):
    reset_url = f"{BASE_URL}/auth/reset-password?token={raw_token}"

    resend.Emails.send({
        "from": SENDER,
        "to": to_email,
        "subject": "Reset your MemeHub password",
        "html": f"""
            <p>You requested a password reset.</p>
            <p><a href="{reset_url}">Click here to reset your password</a></p>
            <p>This link expires in <strong>1 hour</strong>. If you didn't request this, ignore this email.</p>
        """
    })