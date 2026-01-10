from flask import Flask

from .extensions import db, migrate, jwt

from .models.user import User

def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    return app