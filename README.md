# Tiqets Order Processor

## Overview
The Tiqets Order Processor is a full-stack application for managing customers, orders, and barcodes. The backend provides robust data processing and analytics capabilities through RESTful APIs, while the frontend offers an intuitive dashboard for visualizing the data. This project is designed with scalability and reliability in mind, including thorough documentation, tests, and deployment instructions.

---

## Table of Contents
1. [Data Model](docs/data_model/README.md)
2. [API Endpoints](docs/api_endpoints.md)
3. [Testing Guide](docs/testing_guide.md)
4. [Development and Deployment Instructions](docs/dev_and_deployment.md)
5. [Data Validation and Flow](#data-validation-and-flow)
6. [CLI Tool for Data Processing](#cli-tool-for-data-processing)

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
   poetry run alembic -c backend/alembic.ini upgrade head
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

## Data Validation and Flow

### **Data Validation**
The Tiqets Order Processor employs a two-layer validation system to ensure data integrity and reliability:
1. **Pandera**: Used for validating raw CSV input files (e.g., orders, barcodes). It ensures:
   - Strong type checking for DataFrame columns.
   - Custom validation rules (e.g., ensuring unique barcodes).
   - Clear error messages to identify problematic data rows.
   
   **Why Pandera?**
   I chose Pandera because it's specifically designed for DataFrame validation. It provides strong type checking, custom validation rules, and clear error messages—crucial for maintaining data integrity in our ticketing system.

2. **Marshmallow**: Used for API-level validation. Marshmallow ensures:
   - Validity of incoming API request data (e.g., JSON payloads).
   - Serialization and deserialization of Python objects.
   - Schema-based validation for a consistent API contract.

---

### **Data Flow**
The data flow within the Tiqets Order Processor is as follows:
1. **Input Data**:
   - CSV files containing orders and barcodes are uploaded to the system.
   - These files are validated using Pandera before being processed.

2. **Data Processing**:
   - Validated data is merged and transformed using Pandas.
   - Analytics are generated, including:
     - Top customers by ticket count.
     - Unused barcodes in the system.

3. **Database Storage**:
   - Processed data is saved into the PostgreSQL database.
   - Alembic manages schema migrations to ensure the database structure evolves with the application.

4. **API Interaction**:
   - The backend provides RESTful API endpoints for:
     - Fetching processed orders.
     - Viewing analytics like top customers and unused barcodes.
     - Querying customer-specific data.

5. **Frontend Display**:
   - Data is visualized through a React-based dashboard, providing real-time insights into the system.

---
## CLI Tool for Data Processing

A standalone CLI tool is available for batch data processing and debugging. It processes input data, performs analytics, and saves the results for further use.

### **Usage**
Run the script directly to process data, generate analytics, and save the results:
```bash
poetry shell
python backend/tools/main.py
```

### **Features**
- **Data Processing**:
  - Processes raw order and barcode data from CSV files.
  - Handles duplicate barcodes and identifies orders without barcodes.
- **Analytics Generation**:
  - Identifies the top 5 customers by ticket count.
  - Counts and lists unused barcodes in the system.
- **Result Storage**:
  - Saves the processed orders and analytics to the `data/output/processed_orders.csv` file.

### **Sample Output**
Here’s an example of the tool’s output:
```plaintext
2025-01-06 23:42:36,926 - INFO - Starting order processing...
2025-01-06 23:42:36,937 - WARNING - Found 5 duplicate barcodes:
531    11111111649
547    11111111665
...
2025-01-06 23:42:36,942 - ERROR - Found 3 orders without barcodes: [75, 108, 201]

Top 5 customers by number of tickets:
Customer 10: 23
Customer 56: 20
...

Unused barcodes: 98
2025-01-06 23:42:36,962 - INFO - Results saved to data/output/processed_orders.csv
2025-01-06 23:42:36,962 - INFO - Processing completed successfully
```

### **Interrupt Handling**
The script gracefully handles `Ctrl+C` interruptions, ensuring no partial or corrupt data is saved during processing.

### **Error Reporting**
- **Duplicate Barcodes**: The tool logs duplicate barcodes and retains the first occurrence.
- **Orders Without Barcodes**: It identifies and logs orders missing associated barcodes.

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
│   ├── tools/               # CLI tools for standalone processing
│   ├── tests/               # Unit and integration tests
│   └── migrations/          # Database migration scripts
├── frontend/                # React frontend application
│   ├── src/                 # Frontend source code
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page components
│   │   └── services/        # API integration services
│   └── public/              # Static assets
├── data/                    # Input/output data
├── docs/                    # Documentation
└── logs/                    # Log files
```

---

## Features
- **Backend**
  - RESTful API endpoints for data processing.
  - Robust data validation and error handling using Pandera and Marshmallow.
  - PostgreSQL database integration with Alembic migrations.
  - Comprehensive test coverage.

- **Frontend**
  - Interactive dashboard for data visualization.
  - Real-time order processing display.
  - Top customers analytics.
  - Unused barcodes tracking.
  - Responsive design with Tailwind CSS.

---

## Resources
- [Pandera Documentation](https://pandera.readthedocs.io/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [React Documentation](https://reactjs.org/)