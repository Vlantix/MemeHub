from flask import Blueprint, jsonify, request, session
from db.queries.users import get_username, get_email, create_account
from helper import check_password, set_password

auth_bp = Blueprint('auth', __name__)

# ==============================================
# REGISTER API - POST /api/register
# ==============================================
@auth_bp.route('/api/register', methods=['POST'])
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

# ==============================================
# LOGIN API - POST /api/login
# ==============================================
@auth_bp.route('/api/login', methods=['POST'])
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
    
    session['user_id'] = user['id']
    session['username'] = user['username']
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user['id'],
            "display_name": user['display_name'],
            "username": user['username'],
            "email": user['email']
        }
    }), 200

# ==============================================
# LOGOUT API - POST /api/logout
# ==============================================
@auth_bp.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"}), 200