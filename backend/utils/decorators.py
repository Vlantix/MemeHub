from functools import wraps
from flask import request, jsonify
from backend.utils.token import decode_token

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Token is invalid or expired"}), 401

        request.user_id = payload["user_id"]
        request.username = payload["username"]

        return f(*args, **kwargs)
    return decorated