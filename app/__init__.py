from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "default-key")

    from .db import get_db_connection
    app.db_connection = get_db_connection

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.recipe import recipe_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)

    return app