from flask import Blueprint, jsonify, request
from backend.db.queries.posts import get_posts, get_trending_posts
from backend.utils.helper import time_ago
from backend.utils.decorators import login_required

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/feed', methods=['GET'])
@login_required
def get_feed():
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
@login_required
def trending():
    time_filters = {
        'today': '1 day',
        'week':  '7 days',
        'month': '30 days'
    }
    
    try:
        timeframe = request.args.get('timeframe', 'today')
        limit = request.args.get('limit', 10, type=int)
        interval = time_filters.get(timeframe)

        if not interval:
            return jsonify({"error": "Invalid timeframe. Use: today, week, month"}), 400

        posts = get_trending_posts(interval, limit)

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
        
    