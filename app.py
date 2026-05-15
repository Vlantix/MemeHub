from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from config import Config
from db_connection import *
from helper import time_ago, allowed_file, UPLOAD_FOLDER
import os
from datetime import datetime
from routes.main import landing_bp
from routes.auth import auth_bp
from routes.feed import feed_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000  # Limit upload size to 10MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make available to templates
app.jinja_env.globals.update(time_ago=time_ago)

# ==============================================
#       BP ROUTE
# ==============================================
app.register_blueprint(landing_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(feed_bp)

if __name__ == '__main__':
    # Needed to Publish Live
    app.run(port=5001, debug=True)