import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from logging.config import fileConfig

from alembic import context

# Import the application's models and config
from app import db
from app.core.config import Config
from sqlalchemy import engine_from_config, pool

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_database_url():
    """Determine the database URL based on environment."""
    if os.environ.get("DOCKER_MODE"):
        return "postgresql://admin:admin@db:5432/tiqets_db"
    # Try to get URL from environment, fallback to local development URL
    return os.getenv(
        "DATABASE_URL", "postgresql://admin:admin@localhost:5432/tiqets_db"
    )


# Set SQLAlchemy URL
config.set_main_option("sqlalchemy.url", get_database_url())

# Set MetaData object for 'autogenerate' support
target_metadata = db.Model.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well. By skipping the Engine
    creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a
    connection with the context.
    """
    # Get section of alembic.ini config for current environment
    configuration = config.get_section(config.config_ini_section, {})

    # Create SQLAlchemy engine
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Additional useful configs:
            compare_type=True,  # Compare column types
            compare_server_default=True,  # Compare default values
            # Add transaction support
            transaction_per_migration=True,
            # Add error handling for invalid schema changes
            render_as_batch=True,
        )

        try:
            with context.begin_transaction():
                context.run_migrations()
        except Exception as e:
            print(f"Error during migration: {e}")
            raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
