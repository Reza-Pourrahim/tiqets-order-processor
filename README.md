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
- [CI/CD Pipeline](docs/ci_cd.md)

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

## Project Structure

The Tiqets Order Processor follows a well-organized structure that separates concerns and promotes maintainability. Here's a detailed breakdown of the project's architecture:

```bash
tiqets-order-processor/
├── .github/                    # GitHub specific configurations
│   └── workflows/             # GitHub Actions CI/CD workflows
│       ├── ci.yml             # Main CI pipeline configuration
│       ├── deployment.yml     # Deployment workflow configuration
│       └── release.yml        # Release management workflow
│
├── backend/                    # Main backend application code
│   ├── app/                   # Flask application
│   │   ├── api/              # API routes and error handlers
│   │   ├── core/             # Core configurations
│   │   ├── models/           # Database models
│   │   └── schemas/          # Validation schemas
│   ├── src/                  # Core business logic
│   │   ├── data_processing/  # Data processing modules
│   │   │   ├── loader.py     # Data loading functionality
│   │   │   ├── processor.py  # Data processing logic
│   │   │   └── validator.py  # Data validation rules
│   │   └── utils/           # Utility functions
│   │       └── logger.py     # Logging configuration
│   ├── tools/               # CLI tools and scripts
│   │   └── main.py          # Command-line interface
│   ├── tests/               # Test suites
│   │   ├── test_api/        # API endpoint tests
│   │   ├── test_models/     # Database model tests
│   │   ├── test_data_processing/     # Data processing modules tests
│   │   └── conftest.py      # Test configurations
│   ├── migrations/          # Database migrations
│   │   └── versions/        # Migration version files
│   └── alembic.ini          # Migration configuration
│
├── frontend/                  # React frontend application
│   ├── src/                  # Frontend source code
│   │   ├── components/       # Reusable React components
│   │   ├── pages/           # Page-level components
│   │   └── services/        # API integration services
│   ├── public/              # Static assets
│   ├── index.html           # Root HTML template
│   ├── package.json         # Frontend dependencies
│   └── vite.config.js       # Vite configuration
│
├── docker/                    # Docker configuration
│   ├── backend/              # Backend container setup
│   │   └── Dockerfile       # Backend image definition
│   └── frontend/            # Frontend container setup
│       └── Dockerfile       # Frontend image definition
│
├── data/                      # Data directory
│   ├── input/               # Input CSV files
│   │   ├── orders.csv      # Order data
│   │   └── barcodes.csv    # Barcode data
│   └── output/              # Processed results
│
├── docs/                      # Project documentation
│   ├── api_endpoints.md     # API documentation
│   ├── ci_cd.md            # CI/CD pipeline details
│   ├── data_model/         # Data model documentation
│   ├── dev_and_deployment.md # Development guide
│   ├── system_architecture/ # System architecture docs
│   └── testing_guide.md    # Testing documentation
│
├── docker-compose.yml         # Service orchestration
├── Justfile                   # Task runner commands
├── pyproject.toml            # Python dependencies
├── README.md                 # Project documentation
└── .env.example              # Environment template
```

This structure follows several key organizational principles:

1. **Separation of Concerns**: Backend and frontend code are clearly separated, each with their own configuration and dependencies.

2. **Modular Architecture**: The backend is organized into distinct modules (api, core, models, schemas) for better maintainability.

3. **Configuration Management**: Environment variables, Docker configurations, and CI/CD workflows are organized in dedicated directories.

4. **Documentation**: Comprehensive documentation is maintained in the `docs` directory, covering all aspects of the project.

5. **Testing**: Test files are colocated with the code they test, making it easier to maintain and update tests alongside features.

6. **Infrastructure as Code**: Docker configurations and CI/CD workflows are version controlled, ensuring consistent environments.

Each directory serves a specific purpose and contains related files, making the project easy to navigate and maintain. The structure supports both development and production workflows, with clear separation between application code, configuration, and documentation.


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