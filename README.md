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
   # Using Just (recommended)
   just setup    # Build containers
   just start    # Start services
   just migrate  # Run migrations
   ```

   Or using Docker Compose directly:
   ```bash
   docker-compose build
   docker-compose up -d
   docker-compose run backend alembic -c backend/alembic.ini upgrade head
   ```

4. **Access the Application**:
   - Frontend Dashboard: http://localhost:5173
   - Backend API: http://localhost:5000/api

### Alternative: Local Development Setup

If you prefer to run services locally without Docker:

#### Backend Setup
1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Set Environment Variables**:
   ```bash
   cp .env.example .env
   # Update DATABASE_URL if needed
   ```

3. **Run Migrations and Start Server**:
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
just setup          # Build all containers
just start          # Start all services
just stop           # Stop all services
just restart        # Restart services
just migrate        # Run migrations
just test          # Run tests
just logs          # View logs
just backup-db      # Backup database
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

## Resources
- [Pandera Documentation](https://pandera.readthedocs.io/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [React Documentation](https://reactjs.org/)