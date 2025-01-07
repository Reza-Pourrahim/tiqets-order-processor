# Tiqets Order Processor

## Overview
The Tiqets Order Processor is a full-stack application for managing customers, orders, and barcodes. The backend provides robust data processing and analytics capabilities through RESTful APIs, while the frontend offers an intuitive dashboard for visualizing the data. This project is designed with scalability and reliability in mind, including thorough documentation, tests, and deployment instructions.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [Data Validation and Flow](#data-validation-and-flow)
5. [Documentation](#documentation)
6. [CLI Tool](#cli-tool)
7. [Resources](#resources)

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Just (Command Runner) - Optional but recommended
- Git

### Quick Start with Docker (Recommended)

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd tiqets-order-processor
   ```

2. **Environment Setup**:
   ```bash
   cp .env.example .env
   ```

3. **Build and Start Services**:
   ```bash
   # One command setup (recommended)
   just setup-all    # Builds, starts DB, runs migrations, starts all services

   # Or step by step:
   just setup        # Build containers
   just start-db     # Start database and wait for initialization
   just migrate      # Run migrations
   just start        # Start all services
   ```

   Or using Docker Compose directly:
   ```bash
   docker-compose build
   docker-compose up -d db
   sleep 5
   docker-compose run backend alembic -c backend/alembic.ini upgrade head
   docker-compose up -d
   ```

4. **Access the Application**:
   - Frontend Dashboard: http://localhost:5173
   - Backend API: http://localhost:5000/api

### Alternative: Local Development Setup

If you prefer to run services locally without Docker:

1. **Database Setup**:
   ```bash
   # If using local PostgreSQL
   sudo -u postgres psql
   postgres=# CREATE DATABASE tiqets_db;
   postgres=# CREATE USER admin WITH PASSWORD 'admin';
   postgres=# GRANT ALL PRIVILEGES ON DATABASE tiqets_db TO admin;
   ```
   
   Or update your .env file if using Docker's PostgreSQL:
   ```
   DATABASE_URL=postgresql://admin:admin@localhost:5433/tiqets_db
   ```

2. **Install Dependencies**:
   ```bash
   poetry install
   ```

3. **Set Environment Variables**:
   ```bash
   cp .env.example .env
   # Update DATABASE_URL if needed
   ```

4. **Run Migrations and Start Server**:
   ```bash
   poetry run alembic -c backend/alembic.ini upgrade head
   poetry run flask run
   ```

#### Frontend Setup
1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

## Project Structure
```bash
tiqets-order-processor/
├── backend/                 # Main backend code
│   ├── app/                # Flask app
│   │   ├── api/           # API routes and error handlers
│   │   ├── core/          # Core configurations
│   │   ├── models/        # Database models
│   │   └── schemas/       # Validation schemas
│   ├── src/               # Data processing logic
│   │   ├── data_processing/# Data loader and processor
│   │   └── utils/         # Utilities and logging
│   ├── tools/             # CLI tools
│   ├── tests/             # Test suites
│   ├── migrations/        # Database migrations
│   └── alembic.ini        # Migration configuration
├── frontend/              # React frontend application
│   ├── src/               
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   └── services/     # API integration
│   └── vite.config.js    # Vite configuration
├── docker/                # Docker configuration
│   ├── backend/          # Backend Dockerfile
│   └── frontend/         # Frontend Dockerfile
├── data/                 # Data files
│   ├── input/           # Input CSV files
│   └── output/          # Processed results
├── docs/                 # Documentation
├── docker-compose.yml    # Service orchestration
├── Justfile             # Task runner
└── .env.example         # Environment template
```

## Features

### Backend
- RESTful API endpoints for data processing
- Robust data validation using Pandera and Marshmallow
- PostgreSQL database with Alembic migrations
- Comprehensive test coverage
- CLI tool for batch processing

### Frontend
- A dashboard for data visualization
- Real-time order processing display
- Top customers analytics
- Unused barcodes tracking
- Responsive design with Tailwind CSS

## Data Validation and Flow

### Two-Layer Validation
1. **Pandera**: CSV file validation
   - Strong type checking
   - Custom validation rules
   - Clear error messages

2. **Marshmallow**: API validation
   - Request/response validation
   - Schema-based contracts
   - Object serialization

### Data Flow
1. Input: CSV files validated with Pandera
2. Processing: Data merged and transformed
3. Storage: Results saved to PostgreSQL
4. API: RESTful endpoints for data access
5. Frontend: Real-time visualization

## Documentation
Detailed documentation is available in the `docs/` directory:
- [System Architecture](docs/system_architecture/system_architecture.md)
- [Data Model](docs/data_model/README.md)
- [API Endpoints](docs/api_endpoints.md)
- [Testing Guide](docs/testing_guide.md)
- [Development and Deployment](docs/dev_and_deployment.md)

## CLI Tool

### Usage
```bash
poetry shell
python backend/tools/main.py
```

### Features
- Process CSV files
- Generate analytics
- Handle duplicates
- Error reporting

## Available Commands

### Using Just Task Runner
```bash
# Setup and Deployment
just setup-all      # Complete setup: build, start DB, migrate, start services
just setup          # Build all containers
just start-db       # Start only database
just start          # Start all services (interactive)
just start-detached # Start all services in background
just stop           # Stop all services
just restart        # Restart services

# Development
just migrate        # Run migrations
just test          # Run tests
just logs          # View logs
just backend-shell # Access backend container shell
just frontend-shell # Access frontend container shell
just db-shell      # Access database shell

# Database
just backup-db      # Backup database
just migrations-history # View migrations history
just new-migration name # Create new migration

# Maintenance
just clean         # Remove all containers, volumes, and images
just status        # Check container status
```

### Manual Docker Commands
```bash
docker-compose up -d        # Start services
docker-compose down        # Stop services
docker-compose logs -f     # View logs
```

## Testing
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=backend
```

## Troubleshooting

### Common Issues

#### Port Conflicts
If you see an error about port 5432 being in use:
1. Either stop your local PostgreSQL service:
   ```bash
   sudo systemctl stop postgresql
   ```
2. Or use the alternative port (5433) configured in docker-compose.yml

#### Database Connection Issues
- For Docker: Make sure to start the database first: `just start-db`
- For local development: Ensure PostgreSQL is running and the user has proper permissions
- Check if migrations are applied: `just migrate`

#### Container Issues
- If containers fail to start:
  ```bash
  just logs        # Check service logs
  just status      # Check container status
  ```
- For database connection errors, ensure the database is fully initialized
- For a clean restart:
  ```bash
  just clean       # Remove everything
  just setup-all   # Fresh setup
  ```


## Resources
- [Pandera Documentation](https://pandera.readthedocs.io/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [React Documentation](https://reactjs.org/)