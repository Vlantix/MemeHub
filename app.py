from flask import Flask
from config import Config
from routes.main import landing_bp
from routes.auth import auth_bp
from routes.feed import feed_bp
from routes.posts import posts_bp
from routes.profile import profile_bp
from routes.likes import likes_bp
from routes.comments import comments_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000  # Limit upload size to 10MB

# ==============================================
#       BP ROUTE
# ==============================================
app.register_blueprint(landing_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(comments_bp)

if __name__ == '__main__':
    # Needed to Publish Live
    app.run(port=5001, debug=Config.DEBUG)