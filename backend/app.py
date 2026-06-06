from flask import Flask
from backend.config import Config
from backend.routes.main import landing_bp
from backend.routes.auth import auth_bp
from backend.routes.feed import feed_bp
from backend.routes.posts import posts_bp
from backend.routes.profile import profile_bp
from backend.routes.likes import likes_bp
from backend.routes.comments import comments_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000  

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
    app.run(port=5001, debug=Config.DEBUG)