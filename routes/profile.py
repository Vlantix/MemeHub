from flask import Blueprint, jsonify, request, session
from db.db_connection import get_user_profile_by_id, get_user_posts, get_total_likes, update_user_profile

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
def get_user_profile():
    if not session.get('user_id'):
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401

    user_info = get_user_profile_by_id(session['user_id'])
    
    if not user_info:
        return jsonify({
            "error": "User not found"
        }), 404

    user_posts = get_user_posts(session['user_id'], limit=12, offset=0)

    user_data = {
        "user_info": user_info,
        "total_posts": len(get_user_posts(session['user_id'], limit=0, offset=0)),
        "total_likes": sum(get_total_likes(post['id']) for post in user_posts)
    }

    return jsonify({
        "success": True,
        "data": user_data
    }), 200

@profile_bp.route('/profile/update', methods=['PATCH'])
def update_user_info():
    if not session.get('user_id'):
        return jsonify({
            "error": "Authentication Required!",
            "message": "Session expired! Please login"
        }), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user_id = session['user_id']
    current_user = get_user_profile_by_id(user_id)

    if not current_user:
        return jsonify({"error": "User not found"}), 404
    
    update_data = {}
    
    # Handle display_name
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

