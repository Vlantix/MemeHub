from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

database = SQLAlchemy()

class User(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    display_name = database.Column(database.String(80), nullable=False)
    username = database.Column(database.String(80), unique=True, nullable=False)
    email = database.Column(database.String(80), unique=True, nullable=False)
    password_hash = database.Column(database.String(128), nullable=False)
    bio = database.Column(database.Text, nullable=True, default="Your bio here")
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    
    # Relationship to posts
    posts = database.relationship('Post', backref='author', lazy=True)

    # Password handling methods
    def set_password(self, password):
        """Hash the password and store it"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify the password against the hash"""
        return check_password_hash(self.password_hash, password)

class Post(database.Model):
    __tablename__ = 'posts'

    id = database.Column(database.Integer, primary_key=True)
    image_filename = database.Column(database.String(200), nullable=False)
    caption = database.Column(database.Text, nullable=True)
    category = database.Column(database.String(50), nullable=True)
    tags = database.Column(database.String(200), nullable=True)
    visibility = database.Column(database.String(20), default='public')
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    created_at = database.Column(database.DateTime, default=datetime.utcnow)