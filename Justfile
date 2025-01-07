# Lists all available commands when you type `just`
default:
    @just --list

# Builds all the Docker images defined in the docker-compose.yml file
setup:
    docker-compose build

# Starts all services defined in the docker-compose.yml file (Ctrl+C to stop)
start:
    docker-compose up

# Restarts all services
restart:
    docker-compose down && docker-compose up

# Stops all running containers
stop:
    docker-compose down

# Runs the test suite inside the backend service container
test:
    docker-compose run backend pytest

# Runs database migrations using Alembic inside the backend service container
migrate:
    docker-compose run backend alembic -c backend/alembic.ini upgrade head

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

# Backup
backup-db:
    docker-compose exec db pg_dump -U admin tiqets_db > backup_$(date +%Y%m%d).sql