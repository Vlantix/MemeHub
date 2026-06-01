from flask import Blueprint, jsonify, request, make_response
from db.queries.users import get_username, get_email, create_account
from utils.helper import check_password, set_password
from utils.token import generate_access_token, generate_refresh_token, decode_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    display_name = data.get('display_name', '').strip()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    
    if not all([display_name, username, email, password, confirm_password]):
        return jsonify({
            "error": "All fields are required",
            "missing_fields": {
                "display_name": not display_name,
                "username": not username,
                "email": not email,
                "password": not password,
                "confirm_password": not confirm_password
            }
        }), 400
    
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
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = get_username(username)
    
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

    payload = decode_token(refresh_token)
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