from app.core.config import Config
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Register blueprints
    from app.api.routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app