from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

database = SQLAlchemy()

class User(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    display_name = database.Column(database.String(80), nullable=False)
    username = database.Column(database.String(80), unique=True, nullable=False)
    password_hash = database.Column(database.String(128), nullable=False)
    is_active = database.Column(database.Boolean, default=True)
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    updated_at = database.Column(database.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

     # Password handling methods
    def set_password(self, password):
        """Hash the password and store it"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify the password against the hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
