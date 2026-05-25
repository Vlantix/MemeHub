from db.queries.comments import add_comment, get_comments, delete_comment, get_comment_count, update_comment
from routes.posts import get_post
from flask import Blueprint, jsonify, request, session

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def comment_post(post_id):
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401
    
    post = get_post(post_id)
    
    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404
    
    data = request.get_json()
    content = data.get('content', '').strip()

    comment_data = add_comment(user_id, post_id, content)
    comment_count = get_comment_count(post_id)

    if comment_data:
        return jsonify({
            "message": "Add comment on post",
            "commented": True,
            "comment_count": comment_count,
            "comment": {
                "content": content,
                "user_id": user_id,
                "created_at": comment_data['created_at']
            }
        }), 200
    
@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401

    post = get_post(post_id)

    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404
    
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    comments = get_comments(post_id, limit, offset)
    comment_count = get_comment_count(post_id)

    return jsonify({
        "comments": comments,
        "comment_count": comment_count
    }), 200






