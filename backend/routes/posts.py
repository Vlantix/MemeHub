from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request
from backend.db.queries.posts import get_post, create_post, delete_post
from backend.utils.helper import allowed_file
from backend.utils.decorators import login_required
from backend.utils.storage import upload_image, delete_image


posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/post/<int:post_id>', methods=['GET'])
@login_required
def get_single_post(post_id):
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
@login_required
def upload_meme():
    user_id = request.user_id

    if 'meme_image' not in request.files:
        return jsonify({"error": "No file part", "message": "No image selected"}), 400
    
    file = request.files['meme_image']

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type", "message": "Only PNG, JPG, JPEG, GIF, WEBP files are allowed"}), 400

    caption = request.form.get('caption', '')
    category = request.form.get('category', '')
    visibility = request.form.get('visibility', 'public')
    tags_list = request.form.getlist('tags')
    tags = ','.join(tags_list) if tags_list else None

    filename = secure_filename(file.filename)
    file_bytes = file.read()

    uploaded = upload_image(file_bytes, filename)

    if not uploaded:
        return jsonify({"error": "Upload Failed", "message": "Failed to upload image"}), 500

    try:
        new_post = create_post(
            user_id=user_id,
            caption=caption,
            image_filename=uploaded["filename"],
            image_url=uploaded["url"],
            category=category,
            visibility=visibility,
            tags=tags
        )
    except Exception as e:
        delete_image(uploaded["filename"])
        return jsonify({"error": "Server Error", "message": str(e)}), 500

    return jsonify({"success": True, "message": "Post uploaded successfully", "data": new_post}), 201

@posts_bp.route('/delete_post/<int:post_id>', methods=['DELETE'])
@login_required
def delete_meme(post_id):
    user_id = request.user_id

    post = get_post(post_id)

    if not post:
        return jsonify({"error": "Post not found", "message": f"No post found with ID {post_id}"}), 404
    
    if post['user_id'] != user_id:
        return jsonify({"error": "Unauthorized", "message": "You can only delete your own posts"}), 403

    delete_image(post['image_filename'])

    post_deleted = delete_post(post_id, user_id)
    if post_deleted:
        return jsonify({"success": True, "message": "Post deleted successfully"}), 200
    
    return jsonify({
        "error": "Deletion Failed",
        "message": "Failed to delete the post. Please try again."
    }), 500
