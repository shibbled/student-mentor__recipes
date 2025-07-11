from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.secret_key = os.getenv("SECRET_KEY", "default-key")

  # Register Routes
  from app.routes import register_blueprints
  register_blueprints(app)

  return app