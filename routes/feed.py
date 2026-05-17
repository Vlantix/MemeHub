from flask import Blueprint, jsonify, request, session
from db.db_connection import get_posts, get_trending_posts
from helper import time_ago

feed_bp = Blueprint('feed', __name__)

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
    
    time_filters = {
        'today': "p.created_at >= NOW() - INTERVAL 1 DAY",
        'week': "p.created_at >= NOW() - INTERVAL 7 DAY", 
        'month': "p.created_at >= NOW() - INTERVAL 30 DAY"
    }

    try:
        timeframe = request.args.get('timeframe', 'today')
        limit = request.args.get('limit', 10, type=int)
        time_filter = time_filters.get(timeframe, "1=1")

        posts = get_trending_posts(time_filter, limit)

        for post in posts:
            post['time_ago'] = time_ago(post['created_at'])

        return jsonify({
            'success': True,
            'timeframe': timeframe,
            'posts': posts
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e)
        }), 500
        
    