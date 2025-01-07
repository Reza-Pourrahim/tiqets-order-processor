# Use the Python 3.10 slim image as the base
# A minimal Python image for production use
FROM python:3.10-slim

# Set the working directory inside the container
# All subsequent commands will run in this directory
WORKDIR /app

# Copy the dependency files (pyproject.toml and poetry.lock) into the container
# This is done first to leverage Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install Poetry (Python dependency manager) and project dependencies
# - Disable virtualenv creation for Poetry (dependencies installed globally)
# - Use the "--only main" flag to install only the main dependencies (excluding dev dependencies).
# - "--no-root" Flag: This will avoid installing the project itself, only installing the dependencies.
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

# Copy the rest of the application code into the container
# This includes all project files
COPY . .

# Set the default command to run the Flask application
# Flask will serve on 0.0.0.0 to make the service accessible from outside the container
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
