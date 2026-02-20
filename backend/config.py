import os


class Config:
    # MongoDB Configuration
    MONGODB_URI = os.environ.get("MONGODB_URI") or "mongodb+srv://tikaram24_db_user:XFBnTCUsBiT33Tp9@cluster0.yppqcme.mongodb.net/organic_e-ccomerce"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'organic-ecommerce-key'
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'frontend', 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
