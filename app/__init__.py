from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.routes import blueprints
from app.config import Config
from app.scripts import global_init
from app.services import get_user_by_id
from app.models import User
from .routes.api import register_api_routes
from dotenv import load_dotenv


def create_app(testing=False) -> None:
    load_dotenv()
    
    app = Flask(__name__)
    
    app.config.from_object(Config)
    Config.ensure_folders_exist()
    
    csrf = CSRFProtect(app)

    global_init()
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id: int) -> User:
        return get_user_by_id(user_id)
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    register_api_routes(app)
    
    if testing:
        app.config["TESTING"] = True

    return app
