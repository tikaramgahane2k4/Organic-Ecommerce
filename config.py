import os

class Config:
    """Application configuration"""

    # Database Configuration
    if os.environ.get('DATABASE_URL'):
        # Production on Render/Heroku with PostgreSQL
        db_url = os.environ.get('DATABASE_URL')
        # Fix for SQLAlchemy 1.4+ - convert postgres:// to postgresql://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        # Local development with SQLite
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')}"
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder for product images
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
