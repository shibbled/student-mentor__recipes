from .index import index
from .auth import auth

blueprints = [index, auth]

def register_blueprints(app):
  for bp in blueprints:
    app.register_blueprint(bp)
