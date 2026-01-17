import os

class Config:

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://organic_ecommerce_user:rDGwLbP9eQxQNcNgTxYB4ogitEKNtceA@dpg-d5lsv1n5r7bs73cp7g4g-a/organic_ecommerce"
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'organic-ecommerce-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

