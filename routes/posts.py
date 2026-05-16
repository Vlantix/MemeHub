from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request, session
from db_connection import get_post, create_post, delete_post
from helper import allowed_file, UPLOAD_FOLDER
import os

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

@posts_bp.route('/upload', methods=['POST'])
def upload_meme():
    if not session.get('user_id'):
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401
    
    if 'meme_image' not in request.files:
        return jsonify({
            "error": "No file part",
            "message": "No image selected"
        }), 400
    
    file = request.files['meme_image']

    if not file or not allowed_file(file.filename):
        return jsonify({
            "error": "Invalid file type",
            "message": "Only PNG, JPG, JPEG, WEBP files are allowed"
        }), 400
    
    caption = request.form.get('caption', '')
    category = request.form.get('category', '')
    visibility = request.form.get('visibility', 'public')
    tags_list = request.form.getlist('tags')
    tags = ','.join(tags_list) if tags_list else None

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)
    unique_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(filepath)

    try:
        new_post = create_post(
            user_id=session['user_id'],
            caption=caption,
            image_filename=unique_filename,
            category=category,
            visibility=visibility,
            tags=tags
        )

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "error": "Server Error",
            "message": str(e)
        }), 500

    return jsonify({
        "success": True,
        "message": "Post uploaded successfully",
        "data": new_post
    }), 201

@posts_bp.route('/delete_post/<int:post_id>', methods=['DELETE'])
def delete_meme(post_id):
    if not session.get('user_id'):
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401
    
    post = get_post(post_id)

    if post is None:
        return jsonify({
            "error": "Post not found",
            "message": f"No post found with ID {post_id}"
        }), 404
    
    if post and post['user_id'] == session['user_id']:
        try:
            image_path = os.path.join(UPLOAD_FOLDER, post['image_filename'])
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            return jsonify({
                "error": "File Deletion Error",
                "message": f"Post deleted but failed to delete image file: {str(e)}"
            }), 500

        post_deleted = delete_post(post_id, session['user_id'])
        if post_deleted:
            return jsonify({
                "success": True,
                "message": "Post deleted successfully"
            }), 200
        else:
            return jsonify({
                "error": "Deletion Failed",
                "message": "Failed to delete the post. Please try again."
            }), 500
    else:
        return jsonify({
            "error": "Unauthorized",
            "message": "You can only delete your own posts"
        }), 403
