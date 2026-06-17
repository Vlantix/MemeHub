import resend
import os
import logging
from config import Config

logger = logging.getLogger(__name__)


if not Config.RESEND_API_KEY:
    raise ValueError("RESEND_API_KEY is not set in environment variables")
if not Config.RESEND_EMAIL_SENDER:
    raise ValueError("RESEND_EMAIL_SENDER is not set in environment variables")

resend.api_key = Config.RESEND_API_KEY
SENDER = Config.RESEND_EMAIL_SENDER

def send_password_reset_otp(to_email: str, otp: str) -> bool:
    """
    Send OTP email for password reset.
    Returns True if successful, False otherwise.
    """
    try:
        if not to_email or not otp:
            logger.error("Missing email or OTP for password reset")
            return False
            
        response = resend.Emails.send({
            "from": SENDER,
            "to": to_email,
            "subject": "Your MemeHub account password reset code",
            "html": f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .code {{ 
                            font-size: 32px; 
                            letter-spacing: 0.2em; 
                            padding: 15px 30px;
                            background: #f4f4f4;
                            border-radius: 8px;
                            display: inline-block;
                            font-weight: bold;
                            color: #6c5ce7;
                        }}
                        .footer {{ margin-top: 30px; font-size: 14px; color: #888; }}
                        .warning {{ color: #e74c3c; font-weight: bold; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>🔐 Password Reset Request</h2>
                        <p>You requested to reset your password for your MemeHub account.</p>
                        <p>Your verification code is:</p>
                        <div class="code">{otp}</div>
                        <p>This code expires in <strong>15 minutes</strong>.</p>
                        <p class="warning">⚠️ If you didn't request this, please ignore this email.</p>
                        <div class="footer">
                            <p>MemeHub - Social Media Platform for Memes</p>
                            <p>This is an automated message, please do not reply.</p>
                        </div>
                    </div>
                </body>
                </html>
            """
        })
        
        logger.info(f"Password reset OTP sent to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset email to {to_email}: {str(e)}")
        return False