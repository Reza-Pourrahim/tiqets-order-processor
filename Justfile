# Lists all available commands when you type `just`
default:
    @just --list

# Initial setup: builds containers, starts db, runs migrations, and starts all services
setup-all:
    @echo "=== Building containers ==="
    docker-compose build
    @echo "=== Starting database ==="
    docker-compose up -d db
    @echo "=== Waiting for database initialization ==="
    sleep 5
    @echo "=== Running migrations ==="
    docker-compose run backend alembic -c backend/alembic.ini upgrade head
    @echo "=== Starting all services ==="
    docker-compose up -d
    @echo "=== Setup complete! ==="
    @echo "Frontend available at: http://localhost:5173"
    @echo "Backend API available at: http://localhost:5000/api"

# Builds all the Docker images defined in the docker-compose.yml file
setup:
    docker-compose build

# Starts only the database service
start-db:
    docker-compose up -d db
    sleep 5

# Runs database migrations using Alembic inside the backend service container
migrate:
    docker-compose run backend alembic -c backend/alembic.ini upgrade head

# Starts all services defined in the docker-compose.yml file (Ctrl+C to stop)
start:
    docker-compose up

# Starts all services in detached mode
start-detached:
    docker-compose up -d

# Restarts all services
restart:
    docker-compose down
    docker-compose up -d

# Stops all running containers
stop:
    docker-compose down

# Runs the test suite inside the backend service container
test:
    docker-compose run backend pytest

# Streams the logs from all running containers
logs:
    docker-compose logs -f

# Opens a shell in the backend container
backend-shell:
    docker-compose run backend sh

# Opens a shell in the frontend container
frontend-shell:
    docker-compose run frontend sh

# Opens a psql shell in the database container
db-shell:
    docker exec -it tiqets-order-processor-db-1 psql -U admin -d tiqets_db

# Builds only the backend image
build-backend:
    docker-compose build backend

# Builds only the frontend image
build-frontend:
    docker-compose build frontend

# Backup database
backup-db:
    docker-compose exec db pg_dump -U admin tiqets_db > backup_$(date +%Y%m%d).sql

# Clean up everything (containers, volumes, images)
clean:
    docker-compose down -v
    docker system prune -f

# Check status of containers
status:
    docker-compose ps

# View migrations history
migrations-history:
    docker-compose run backend alembic -c backend/alembic.ini history

# Create a new migration
new-migration name:
    docker-compose run backend alembic -c backend/alembic.ini revision --autogenerate -m "{{name}}"