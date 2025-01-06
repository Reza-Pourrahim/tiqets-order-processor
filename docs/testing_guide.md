# Testing Guide

## Overview
This guide provides detailed instructions on how to run tests for the Tiqets Order Processor. The testing suite ensures that the application is robust, reliable, and production-ready.

---

## Prerequisites
1. Ensure all dependencies are installed:
   ```bash
   poetry install
   ```

2. Confirm that your database is configured correctly:
   - Use a separate test database to avoid overwriting production data.
   - Update the `.env` file with the test database connection string.

---

## Running Tests
### Run All Tests
To execute the full test suite:
```bash
poetry run pytest
```

### Run Tests with Coverage Report
To view the test coverage:
```bash
poetry run pytest --cov=backend
```

### Run Specific Tests
You can run a specific test file or test case:
```bash
poetry run pytest backend/tests/test_api/test_routes.py
poetry run pytest backend/tests/test_api/test_routes.py::test_process_orders_endpoint
```

---

## Test Coverage
The test suite is designed to cover the following areas:

### 1. **API Endpoints**
- Validates the behavior of all API routes.
- Ensures proper handling of query parameters and path parameters.
- Confirms error handling and response formats.

### 2. **Data Processing**
- Ensures correctness of the data processing logic, including:
  - Order merging.
  - Barcode validation.
  - Analytics (top customers and unused barcodes).

### 3. **Data Models**
- Validates the database models and their relationships.
- Ensures constraints (e.g., unique and foreign keys) are enforced.

### 4. **Unit Tests**
- Covers individual utility functions and classes, such as:
  - The data loader.
  - Validation logic.

---

## Testing Directory Structure
The tests are organized as follows:
```
backend/tests/
├── test_api/                 # API endpoint tests
│   ├── test_routes.py        # Tests for API routes
│
├── test_data_processing/     # Data processing tests
│   ├── test_loader.py        # Tests for data loading
│   ├── test_processor.py     # Tests for data processing logic
│   ├── test_validator.py     # Tests for validation logic
│
├── test_models/              # Database model tests
│   ├── test_models.py        # Tests for customer, order, and barcode models
│
├── conftest.py               # Fixtures and shared setup
```

---

## Key Test Cases
Below are some of the critical test cases included in the suite:

### **API Tests**
- **Test Process Orders Endpoint**:
  - Validates the `/api/process` route for correct processing and analytics.
  - Ensures proper error handling.

- **Test Top Customers Endpoint**:
  - Validates the `/api/customers/top` route with and without query parameters.
  - Tests invalid inputs and ensures they result in `400 Bad Request`.

- **Test Unused Barcodes Endpoint**:
  - Ensures the `/api/barcodes/unused` route correctly identifies unused barcodes.

- **Test Customer Orders Endpoint**:
  - Validates `/api/orders/<customer_id>` for both existing and non-existent customers.

---

## Notes
1. Always run the tests in a controlled environment (e.g., a test database) to avoid data loss or corruption.
2. Test data is loaded using fixtures in `conftest.py` to ensure consistency across test runs.
3. For CI/CD pipelines, integrate the test suite to ensure code quality and prevent regressions.

---

## Example Commands for CI/CD Integration
### Install Dependencies
```bash
poetry install
```

### Run Tests
```bash
poetry run pytest --cov=backend
```

### Enforce Code Quality
Use linters such as `flake8` and formatters such as `black`:
```bash
poetry run flake8 backend
poetry run black --check backend
```
