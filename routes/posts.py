from flask import Blueprint, jsonify, request, session
from db_connection import get_post

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/post/<int:post_id>', methods=['GET'])
def get_single_post(post_id):
    if not session.get('user_id'):
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401
    
    post = get_post(post_id)
    
    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404
    
    return jsonify({
        "success": True,
        "data": post
    }), 200