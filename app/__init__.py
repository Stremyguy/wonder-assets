from flask import Flask
from app.routes import blueprints
from app.config import Config
from app.scripts import db_session
from .routes.api import register_api_routes

from dotenv import load_dotenv


load_dotenv()


def create_app(testing=False) -> None:
    app = Flask(__name__)
    app.config.from_object(Config)
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    register_api_routes(app)
    
    db_session.global_init()
    
    if testing:
        app.config["TESTING"] = True
    
    return app
