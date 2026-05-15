from flask import Blueprint, flash, jsonify, request, session, url_for
from db_connection import get_posts, get_post

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/post/<int:post_id>', methods=['GET'])
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

@feed_bp.route('/feed', methods=['GET'])
def get_feed():
    if not session.get('user_id'):
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401

    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)   

    posts = get_posts(limit, offset)

    if not posts:
        return jsonify({
            "error": "No uploaded posts yet"
        }), 404

    return jsonify({
        "success": True,
        "data": posts,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "has_more": len(posts) == limit
        }
    }), 200
    
@feed_bp.route('/trending', methods=['GET'])
def trending():
    if not session.get('user_id'):
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401
    
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)   
        
    