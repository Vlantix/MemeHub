from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def time_ago(date):
    """Convert datetime to 'X hours ago' format"""
    now = datetime.utcnow()
    diff = now - date
    
    if diff.days > 0:
        if diff.days == 1:
            return "Yesterday"
        return f"{diff.days} days ago"
    elif diff.seconds // 3600 > 0:
        hours = diff.seconds // 3600
        if hours == 1:
            return "1 hour ago"
        return f"{hours} hours ago"
    elif diff.seconds // 60 > 0:
        minutes = diff.seconds // 60
        if minutes == 1:
            return "1 minute ago"
        return f"{minutes} minutes ago"
    else:
        return "Just now"
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS