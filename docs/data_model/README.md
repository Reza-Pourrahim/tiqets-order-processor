# Data Model Documentation

This folder contains the data model for the Tiqets order processing system.

## Data Model Diagram

![Data Model](data_model.png)

## Entity Descriptions
- **Customer**: Represents a customer with fields like `id`, `email`, and `name`.
- **Order**: Tracks orders placed by customers.
- **Barcode**: Represents individual barcodes associated with orders.

## Relationships
1. **Customer → Order**: One-to-Many
2. **Order → Barcode**: One-to-Many
