from db.queries.comments import add_comment, get_comments, delete_comment, get_comment_count, update_comment
from routes.posts import get_post
from flask import Blueprint, jsonify, request
from utils.decorators import login_required

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def comment_post(post_id):
    user_id = request.user_id

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
    else:
        return jsonify({
            "message": "Failed to add comment",
            "commented": False
        }), 400
    
@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@login_required
def get_post_comments(post_id):
    user_id = request.user_id
    post = get_post(post_id)

    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404
    
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    comments = get_comments(post_id, limit, offset, user_id)
    comment_count = get_comment_count(post_id)

    return jsonify({
        "comments": comments,
        "comment_count": comment_count
    }), 200

@comments_bp.route('/posts/comments/<int:comment_id>', methods=['PATCH'])
@login_required
def edit_comment(comment_id):
    user_id = request.user_id
    
    data = request.get_json()
    content = data.get('content', '').strip()

    success = update_comment(comment_id, user_id, content)

    if success:
        return jsonify({
            "message": "Comment updated",
            "updated": True,
            "comment": {
                "content": content,
                "user_id": user_id
            }
        }), 200

    return jsonify({
        "message": "Comment not found or unauthorized",
        "updated": False
    }), 404

@comments_bp.route('/posts/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def remove_comment(comment_id):
    user_id = request.user_id
    
    success = delete_comment(comment_id, user_id)

    if success:
        return jsonify({
            "message": "Comment deleted",
            "deleted": True
        }), 200

    return jsonify({
        "message": "Comment not found or unauthorized",
        "deleted": False
    }), 404