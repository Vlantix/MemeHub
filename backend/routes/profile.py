from flask import Blueprint, jsonify, request
from db.queries.profile import (
    get_user_profile_by_id, get_user_posts, get_total_likes,
    update_user_profile, get_total_posts,
    update_profile_photo, update_cover_photo, get_user_photo_filenames
)
from utils.decorators import login_required
from utils.helper import validate_image
from utils.storage import delete_image, upload_image


profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@login_required
def get_user_profile():
    user_id = request.user_id

    user_info = get_user_profile_by_id(user_id)
    
    if not user_info:
        return jsonify({
            "error": "User not found"
        }), 404

    user_posts = get_user_posts(user_id, limit=12, offset=0)
    total_likes = get_total_likes(user_id)

    user_data = {
        "user_info": user_info,
        "total_posts": get_total_posts(user_id),
        "total_likes": total_likes,
        "recent_posts": user_posts
    }

    return jsonify({
        "success": True,
        "data": user_data
    }), 200

@profile_bp.route('/profile/update', methods=['PATCH'])
@login_required
def update_user_info():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user_id = request.user_id
    current_user = get_user_profile_by_id(user_id)

    if not current_user:
        return jsonify({"error": "User not found"}), 404
    
    update_data = {}
    
    display_name = data.get('display_name', '').strip()
    if display_name and display_name != current_user['display_name']:
        if len(display_name) < 3:
            return jsonify({"error": "Display name must be at least 3 characters"}), 400
        if len(display_name) > 50:
            return jsonify({"error": "Display name must be less than 50 characters"}), 400
        update_data['display_name'] = display_name
    
    # Handle bio
    if 'bio' in data:
        bio = data.get('bio', '').strip()
        if len(bio) > 160:
            return jsonify({"error": "Bio must be less than 160 characters"}), 400
        if bio != current_user.get('bio', ''):
            update_data['bio'] = bio
    
    if not update_data:
        return jsonify({"error": "No changes to update"}), 400
    
    success = update_user_profile(
        user_id, 
        update_data.get('display_name'), 
        update_data.get('bio')
    )
    
    if success:
        updated_user = get_user_profile_by_id(user_id)
        return jsonify({
            "success": True, 
            "message": "Profile updated successfully",
            "user_info": updated_user
        }), 200
    else:
        return jsonify({"error": "Failed to update profile"}), 500
    
@profile_bp.route('/profile/photo', methods=['PATCH'])
@login_required
def update_profile_photo_route():
    user_id = request.user_id

    file = request.files.get('photo')
    error = validate_image(file)
    if error:
        return jsonify({"error": error}), 400

    file_bytes = file.read()
    result = upload_image(file_bytes, file.filename)
    if not result:
        return jsonify({"error": "Failed to upload image"}), 500

    filenames = get_user_photo_filenames(user_id)
    if filenames and filenames.get('profile_photo_filename'):
        delete_image(filenames['profile_photo_filename'])

    update_profile_photo(user_id, result['url'], result['filename'])

    return jsonify({
        "success": True,
        "message": "Profile photo updated successfully",
        "profile_photo_url": result['url']
    }), 200


@profile_bp.route('/profile/cover', methods=['PATCH'])
@login_required
def update_cover_photo_route():
    user_id = request.user_id

    file = request.files.get('photo')
    error = validate_image(file)
    if error:
        return jsonify({"error": error}), 400

    file_bytes = file.read()
    result = upload_image(file_bytes, file.filename)
    if not result:
        return jsonify({"error": "Failed to upload image"}), 500

    filenames = get_user_photo_filenames(user_id)
    if filenames and filenames.get('cover_photo_filename'):
        delete_image(filenames['cover_photo_filename'])

    update_cover_photo(user_id, result['url'], result['filename'])

    return jsonify({
        "success": True,
        "message": "Cover photo updated successfully",
        "cover_photo_url": result['url']
    }), 200

