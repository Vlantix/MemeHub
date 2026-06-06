import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")
SENDER = os.getenv("RESEND_SENDER_EMAIL")

def send_password_reset_otp(to_email: str, otp: str) -> None:
    resend.Emails.send({
        "from": SENDER,
        "to": to_email,
        "subject": "Your MemeHub account password reset code",
        "html": f"""
            <p>You requested a password reset.</p>
            <p>Your verification code is:</p>
            <h2 style="letter-spacing: 0.2em;">{otp}</h2>
            <p>This code expires in <strong>15 minutes</strong>.
               If you didn't request this, you can safely ignore this email.</p>
        """
    })