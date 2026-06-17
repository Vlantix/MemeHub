from flask import Blueprint, jsonify, request, make_response
from db.queries.users import get_username, get_email, create_account
from db.queries.reset_password import create_otp, verify_otp, update_password
from utils.helper import check_password, set_password
from utils.token import generate_access_token, generate_refresh_token, decode_token, generate_reset_session_token
from utils.email import send_password_reset_otp
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    display_name = data.get('display_name', '').strip()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    
    if not display_name:
        return jsonify({"error": "Display name is required"}), 400
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    if not email:
        return jsonify({"error": "Email is required"}), 400

    if len(display_name) < 3:
        return jsonify({"error": "Display name must be at least 3 characters"}), 400
    
    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    
    if '@' not in email or '.' not in email:
        return jsonify({"error": "Invalid email format"}), 400
    
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400
    
    existing_user = get_username(username)
    if existing_user:
        return jsonify({"error": "Username is already taken"}), 409
    
    existing_email = get_email(email)
    if existing_email:
        return jsonify({"error": "Email is already registered"}), 409
    
    password_hash = set_password(password)
    user_id = create_account(display_name, username, email, password_hash)
    
    return jsonify({
        "success": True,
        "message": "Account created successfully",
        "user": {
            "id": user_id,
            "display_name": display_name,
            "username": username,
            "email": email
        }
    }), 201

@auth_bp.route('/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    username_or_email = data.get('username_or_email', '').strip()
    password = data.get('password', '')
    
    if not username_or_email or not password:
        return jsonify({"error": "Username/email and password are required"}), 400
    
    user = get_username(username_or_email) or get_email(username_or_email)
    
    if not user or not check_password(user['password_hash'], password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = generate_access_token(user['id'], user['username'])
    refresh_token = generate_refresh_token(user['id'], user['username'])
    
    response = make_response(jsonify({
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user['id'],
            "display_name": user['display_name'],
            "username": user['username'],
            "email": user['email']
        }
    }), 200)

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=7 * 24 * 60 * 60
    )
    
    return response
    
@auth_bp.route('/auth/refresh', methods=['POST'])
def token_refresh():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "Refresh token missing"}), 401

    payload = decode_token(refresh_token, expected_type="refresh")
    if not payload:
        return jsonify({"error": "Refresh token invalid or expired"}), 401

    new_access_token = generate_access_token(payload["user_id"], payload["username"])

    return jsonify({
        "success": True,
        "access_token": new_access_token
    }), 200

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200)

    response.delete_cookie("refresh_token")
    return response

@auth_bp.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    user = get_email(email)

    if user:
        try:
            otp = create_otp(user['id'])
            email_sent = send_password_reset_otp(email, otp)

            if not email_sent:
                logger.error(f"Failed to send OTP to {email} but user exists")
        
        except Exception as e:
            logger.error(f"Error in forgot password flow for {email}: {str(e)}")

    return jsonify({
        "message": "If an account with that email exists, a reset code has been sent."
    }), 200

@auth_bp.route('/auth/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    otp = data.get('otp', '').strip()

    if not otp:
        return jsonify({"error": "OTP is required"}), 400
    
    user_id = verify_otp(otp)

    if not user_id:
        return jsonify({"error": "Invalid or expired code"}), 400

    reset_token = generate_reset_session_token(user_id)

    return jsonify({
        "success": True,
        "reset_token": reset_token
    }), 200

@auth_bp.route('/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    reset_token = data.get("reset_token", "").strip()
    new_password = data.get("new_password", "")

    if not reset_token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    if len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    
    payload = decode_token(reset_token, expected_type="password_reset")

    if not payload:
        return jsonify({"error": "Invalid or expired token"}), 400
    
    new_password_hash = set_password(new_password)
    update_password(payload["user_id"], new_password_hash)

    return jsonify({
        "success": True,
        "message": "Password has been reset successfully"
    }), 200





