from app.core.config import Config
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    ma.init_app(app)
    CORS(app)

    # Blueprints
    from app.api.routes import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
