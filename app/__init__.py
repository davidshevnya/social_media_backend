from flask import Flask

from .extensions import db, migrate, jwt
from .models.user import User
from .cli import register_cli


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    register_cli(app)
    
    from .routes.auth import auth_bp
    
    app.register_blueprint(auth_bp)
    
    return app