import os
from flask import Flask
from flask_cors import CORS
from config import Config
from db.connection import validate_schema
from routes.main import landing_bp
from routes.auth import auth_bp
from routes.feed import feed_bp
from routes.posts import posts_bp
from routes.profile import profile_bp
from routes.likes import likes_bp
from routes.comments import comments_bp

def validate_environment():
    """Validate all configurations before starting"""
    try:
        Config.validate()
        validate_schema()
        print("✅ All validations passed!")
        return True
    except Exception as e:
        print(f"❌ Validation Failed: {e}")
        return False

if not validate_environment():
    print("❌ Exiting due to validation failure")
    exit(1)

app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000

allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5500,http://127.0.0.1:5500').split(',')

CORS(app, 
     supports_credentials=True, 
     origins=allowed_origins,
     methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With']
)

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

@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)