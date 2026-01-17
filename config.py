import os

class Config:

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://postgres:Database%40123@localhost:5432/Organic-Ecommerce.db"
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'organic-ecommerce-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

