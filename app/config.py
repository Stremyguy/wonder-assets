import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    
    # Subdirectories
    PROFILE_PICS_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "profile_pics")
    ITEMS_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "items")
    IMAGES_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "images/items")
    
    @classmethod
    def ensure_folders_exist(cls: "Config") -> None:
        """Create all required upload folders on startup"""
        Path(cls.BASE_UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
        Path(cls.PROFILE_PICS_FOLDER).mkdir(parents=True, exist_ok=True)
        Path(cls.ITEMS_FOLDER).mkdir(parents=True, exist_ok=True)
        Path(cls.IMAGES_FOLDER).mkdir(parents=True, exist_ok=True)