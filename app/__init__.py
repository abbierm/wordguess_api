from config import Config
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    db.init_app(app)
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app



from . import wordguess
from app import models