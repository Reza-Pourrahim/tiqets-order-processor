# Tiqets Order Processor

## Overview
The Tiqets Order Processor is a full-stack application for managing customers, orders, and barcodes. The backend provides robust data processing and analytics capabilities through RESTful APIs, while the frontend offers an intuitive dashboard for visualizing the data. This project is designed with scalability and reliability in mind, including thorough documentation, tests, and deployment instructions.

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
- **Poetry** for backend dependency management
- **Node.js 16 or later** for frontend development
- **PostgreSQL** as the database

### Steps to Run Locally

#### Backend Setup
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd tiqets-order-processor
   ```

2. **Install Backend Dependencies**:
   ```bash
   poetry install
   ```

3. **Set Environment Variables**:
   - Create a `.env` file from the provided example configuration:
     ```bash
     cp .env.example .env
     ```
   - Add the following environment variables:
     ```env
     # Flask Configuration
     FLASK_APP=backend/wsgi.py
     FLASK_ENV=development

     # Database Configuration
     DATABASE_URL=postgresql://admin:admin@localhost:5432/tiqets_db
     ```

4. **Apply Database Migrations**:
   ```bash
   poetry run alembic upgrade head
   ```

5. **Run the Backend**:
   ```bash
   poetry run flask run
   ```

#### Frontend Setup
1. **Install Frontend Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run the Frontend Development Server**:
   ```bash
   npm run dev
   ```

The application will be accessible at:
- Backend API: http://localhost:5000
- Frontend Dashboard: http://localhost:5173

---

## Testing
### Backend Tests
```bash
poetry run pytest
```

---

## Project Structure
```
tiqets-order-processor/
├── backend/                 # Main backend code
│   ├── app/                 # Flask app
│   ├── src/                 # Data processing logic
│   ├── tests/              # Unit and integration tests
│   └── migrations/         # Database migration scripts
├── frontend/               # React frontend application
│   ├── src/               # Frontend source code
│   │   ├── components/    # Reusable React components
│   │   ├── pages/        # Page components
│   │   └── services/     # API integration services
│   └── public/           # Static assets
├── data/                  # Input/output data
├── docs/                  # Documentation
└── logs/                  # Log files
```

---

## Features
- **Backend**
  - RESTful API endpoints for data processing
  - Robust data validation and error handling
  - PostgreSQL database integration
  - Comprehensive test coverage

- **Frontend**
  - Interactive dashboard for data visualization
  - Real-time order processing display
  - Top customers analytics
  - Unused barcodes tracking
  - Responsive design with Tailwind CSS