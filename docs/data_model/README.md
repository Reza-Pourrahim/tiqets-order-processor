# Data Model Documentation

## Overview
The data model for the Tiqets Order Processor represents the relationships between customers, orders, and barcodes. It is designed to ensure efficient handling of order processing and analytics.

---

## Data Model Diagram

Below is the diagram illustrating the relationships between the entities:

![Data Model](data_model.png)

---

## Entity Descriptions

### **Customer**
Represents a customer in the system.
- **Attributes**:
  - `id (PK)`: Unique identifier for the customer (Integer).
  - `email`: Customer's email address (String, unique).
  - `name`: Customer's name (String).
  - `created_at`: Timestamp of customer creation.
  - `updated_at`: Timestamp of the last update to the customer.

---

### **Order**
Represents an order placed by a customer.
- **Attributes**:
  - `id (PK)`: Unique identifier for the order (Integer).
  - `customer_id (FK)`: Reference to the `Customer` entity (Integer).
  - `created_at`: Timestamp of order creation.
  - `updated_at`: Timestamp of the last update to the order.

---

### **Barcode**
Represents a barcode associated with an order.
- **Attributes**:
  - `id (PK)`: Unique identifier for the barcode (Integer).
  - `barcode_value`: Unique value of the barcode (String, unique).
  - `order_id (FK)`: Reference to the `Order` entity (Integer).
  - `is_used`: Boolean indicating if the barcode has been used.
  - `created_at`: Timestamp of barcode creation.
  - `updated_at`: Timestamp of the last update to the barcode.

---

## Relationships

### 1. **Customer → Order**
- **Type**: One-to-Many
- **Details**: Each customer can place multiple orders.

### 2. **Order → Barcode**
- **Type**: One-to-Many
- **Details**: Each order can have multiple associated barcodes.

---

## Database Schema (Optional)
You can include an SQL-like schema definition if needed:
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE barcodes (
    id SERIAL PRIMARY KEY,
    barcode_value VARCHAR(255) UNIQUE NOT NULL,
    order_id INTEGER REFERENCES orders(id),
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Usage
This data model is used in the Tiqets Order Processor to:
- Manage customer information.
- Track orders and their associated barcodes.
- Perform analytics, such as identifying top customers or unused barcodes.

