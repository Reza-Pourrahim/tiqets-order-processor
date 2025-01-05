import os
from pathlib import Path


class Config:
    # Base directory of the application
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + str(
        BASE_DIR / "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File paths
    INPUT_DIR = BASE_DIR / "data" / "input"
    OUTPUT_DIR = BASE_DIR / "data" / "output"
