from flask import Flask
from app.routes import blueprints


def create_app() -> None:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "supersecretkey"
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    return app
