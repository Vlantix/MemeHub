from db.queries.likes import add_like, remove_like, check_user_liked, get_post_like_count, get_users_who_liked
from db.queries.posts import get_post
from flask import Blueprint, jsonify, request
from utils.decorators import login_required

likes_bp = Blueprint('likes', __name__)

@likes_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    user_id = request.user_id
    post = get_post(post_id)
    
    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404
    
    success = add_like(user_id, post_id)
    like_count = get_post_like_count(post_id)

    if success:
        return jsonify({
            "message": "Post liked",
            "liked": True,
            "like_count": like_count
        }), 200

    return jsonify({
        "message": "Already liked",
        "liked": True,
        "like_count": like_count
    }), 400

@likes_bp.route('/posts/<int:post_id>/unlike', methods=['POST'])
@login_required
def unlike_post(post_id):
    user_id = request.user_id
    post = get_post(post_id)

    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404

    success = remove_like(user_id, post_id)
    like_count = get_post_like_count(post_id)

    if success:
        return jsonify({
            "message": "Post unliked",
            "unliked": True,
            "like_count": like_count
        }), 200

    return jsonify({
        "message": "Like not found", 
        "liked": False, 
        "like_count": like_count
    }), 404

@likes_bp.route('/posts/<int:post_id>/status', methods=['GET'])
@login_required
def get_like_status(post_id):
    user_id = request.user_id

    liked = check_user_liked(user_id, post_id)
    like_count = get_post_like_count(post_id)

    return jsonify({
        "liked": liked,
        'like_count': like_count
    }), 200

@likes_bp.route('/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    limit = request.args.get('limit', 10, type=int)
    users = get_users_who_liked(post_id, limit)
    like_count = get_post_like_count(post_id)
    
    return jsonify({
        "post_id": post_id,
        "like_count": like_count,
        "users": users
    }), 200