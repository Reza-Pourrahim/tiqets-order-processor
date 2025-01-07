# Development and Deployment Guide

## Overview

This document outlines how to set up, run, and develop the Tiqets Order Processor. The application uses Docker for containerization, ensuring consistent behavior across different environments.

## Prerequisites

- Docker and Docker Compose
- Just (Command Runner) - Optional but recommended
- Git

## Project Structure

```bash
tiqets-order-processor/
├── docker/                # Docker configuration
│   ├── backend/          # Backend Dockerfile and configs
│   └── frontend/         # Frontend Dockerfile and configs
├── docker-compose.yml    # Service orchestration
└── Justfile             # Task runner for common operations
```

## Getting Started

### 1. Clone and Configure

```bash
# Clone the repository
git clone <repository_url>
cd tiqets-order-processor

# Set up environment configuration
cp .env.example .env
```

### 2. Build and Start Services

Using Just (recommended):

```bash
# Complete setup with one command
just setup-all   # Builds, starts DB, runs migrations, starts services

# Or step by step approach:
just setup       # Build containers
just start-db    # Start database and wait for initialization
just migrate     # Run migrations
just start       # Start services (interactive mode)
# or
just start-detached  # Start services in background
```

Or using Docker Compose directly:

```bash
docker-compose build
docker-compose up -d
docker-compose run backend alembic -c backend/alembic.ini upgrade head
```

### 3. Access the Application

After starting the services, the application will be available at:

**Frontend**:

- Local development: [http://localhost:5173](http://localhost:5173)
- Network access: http\://[your-ip]:5173

**Backend API**:

- Local access: [http://localhost:5000/api](http://localhost:5000/api)
- Network access: http\://[your-ip]:5000/api

### 4. Using the Application

1. Visit [http://localhost:5173/](http://localhost:5173/) to access the dashboard, which shows:

   - Processed orders (uses `/api/process`)
   - Top customers (uses `/api/customers/top`)
   - Unused barcodes (uses `/api/barcodes/unused`)

2. Available API endpoints (can be tested directly):

   ```bash
   # Process all orders and get analytics
   curl http://localhost:5000/api/process

   # Get top customers
   curl http://localhost:5000/api/customers/top

   # Get unused barcodes
   curl http://localhost:5000/api/barcodes/unused

   # Get orders for a specific customer (replace 101 with customer ID)
   curl http://localhost:5000/api/orders/10
   ```

---

## Common Operations

### Available Just Commands

#### Setup and Deployment
```bash
just setup-all      # Complete setup process
just setup          # Build containers
just start-db       # Start database only
just start          # Start all services (interactive)
just start-detached # Start all services in background
just stop           # Stop all services
just restart        # Restart services
```

#### Development
```bash
just migrate        # Run migrations
just test          # Run tests
just logs          # View logs
just backend-shell # Access backend shell
just frontend-shell # Access frontend shell
just db-shell      # Access database shell
```

#### Database Operations
```bash
just backup-db      # Backup database
just migrations-history # View migrations history
just new-migration name # Create new migration
```

#### Maintenance
```bash
just clean         # Remove all containers, volumes, and images
just status        # Check container status
```

### Manual Docker Commands

If not using Just:

```bash
docker-compose up -d        # Start services
docker-compose down         # Stop services
docker-compose logs -f      # View logs
```

---

## Container Details

### Database (PostgreSQL)

- Image: postgres:15
- Default credentials:
  - Database: tiqets\_db
  - User: admin
  - Password: admin
- Data persisted via Docker volume

### Backend (Python/Flask)

- Python 3.10 with Poetry dependency management
- Exposed on port 5000
- RESTful API with data processing capabilities

### Frontend (React)

- Node.js 18 with Vite build tool
- Exposed on port 5173
- Real-time data visualization dashboard

---

## Development Workflow

1. **Setup**: Ensure all services are running

   ```bash
   just start
   just migrate
   ```

2. **Development**:

   - Make code changes
   - Run tests: `just test`
   - Check logs: `just logs`
   - Restart if needed: `just restart`

3. **Database Management**:

   - Create backup: `just backup-db`
   - Apply migrations: `just migrate`

---


## Troubleshooting

- If services don't start: 
  ```bash
  just logs        # Check service logs
  just status      # Check container status
  ```
- For database issues:
  ```bash
  just start-db    # Restart database
  just migrate     # Rerun migrations
  ```
- For clean restart:
  ```bash
  just clean       # Remove everything
  just setup-all   # Fresh setup
  ```