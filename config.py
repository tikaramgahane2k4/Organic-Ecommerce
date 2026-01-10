import os

class Config:
    """Application configuration"""

    # SQLite Database Configuration (Local)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')}"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder for product images
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
