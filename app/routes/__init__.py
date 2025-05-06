from .auth import auth_bp
from .profile import profile_bp
from .categories import category_bp
from .admin_panel import admin_bp
from .items import item_bp
from .files import file_bp

blueprints = [auth_bp, profile_bp, category_bp, admin_bp, item_bp, file_bp]