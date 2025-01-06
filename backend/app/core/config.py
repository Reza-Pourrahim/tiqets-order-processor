import os
from pathlib import Path


class Config:
    # Base directory of the application (points to tiqets_order_processor/)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    # File paths
    INPUT_DIR = BASE_DIR / "data" / "input"
    OUTPUT_DIR = BASE_DIR / "data" / "output"

    # Database
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://admin:admin@localhost:5432/tiqets_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        False  # To reduce memory usage and improve performance
    )
