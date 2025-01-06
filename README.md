# Tiqets Order Processor

## Overview
The Tiqets Order Processor is a production-ready backend system for managing customers, orders, and barcodes. It includes features for data processing, analytics, and API endpoints. This project is designed with scalability and reliability in mind, and includes thorough documentation, tests, and deployment instructions.

---

## Table of Contents
1. [Data Model](docs/data_model/README.md)
2. [API Endpoints](docs/api_endpoints.md)
3. [Testing Guide](docs/testing_guide.md)
4. [Development and Deployment Instructions](docs/dev_and_deployment.md)

---

## Quickstart Guide

### Prerequisites
- **Python 3.10 or later**
- **Poetry** for dependency management
- **PostgreSQL** as the database

### Steps to Run Locally
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd tiqets-order-processor
   ```

2. **Install Dependencies**:
   ```bash
   poetry install
   ```

3. **Set Environment Variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your database configuration.

4. **Apply Database Migrations**:
   ```bash
   poetry run alembic upgrade head
   ```

5. **Run the Application**:
   ```bash
   poetry run flask run
   ```

The application will be accessible at `http://localhost:5000`.

---

## Testing
Run the tests to ensure everything is working:
```bash
poetry run pytest
```

---

## Deployment
Refer to the [Development and Deployment Instructions](docs/dev_and_deployment.md) for detailed deployment steps, including Docker setup.

---

## Project Structure
```
tiqets-order-processor/
├── backend/                 # Main backend code
│   ├── app/                 # Flask app
│   ├── src/                 # Data processing logic
│   ├── tests/               # Unit and integration tests
│   └── migrations/          # Database migration scripts
├── data/                    # Input/output data
├── docs/                    # Documentation
├── docker/                  # Docker configuration
└── logs/                    # Log files
```