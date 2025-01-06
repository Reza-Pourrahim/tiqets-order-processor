# API Endpoints Documentation

## Overview
This document provides detailed information about the REST API endpoints available in the Tiqets Order Processor. These endpoints allow for processing orders, fetching analytics, and managing customer and barcode data.

---

## Table of Contents
1. [Process Orders](#1-process-orders)
2. [Get Top Customers](#2-get-top-customers)
3. [Get Unused Barcodes](#3-get-unused-barcodes)
4. [Get Customer Orders](#4-get-customer-orders)

---

## 1. Process Orders
- **Endpoint**: `/api/process`
- **Method**: `GET`
- **Description**: Processes the order and barcode data and returns results with processed orders and analytics.
- **Response**:
    ```json
    {
        "status": "success",
        "data": {
            "orders": [
                {
                    "customer_id": 1,
                    "order_id": 101,
                    "barcodes": [12345, 67890]
                }
            ],
            "analytics": {
                "top_customers": [
                    {
                        "customer_id": 1,
                        "ticket_count": 5
                    }
                ],
                "unused_barcodes": {
                    "count": 10,
                    "barcodes": [
                        {
                            "barcode": 54321,
                            "order_id": null
                        }
                    ]
                }
            }
        }
    }
    ```
- **Error Responses**:
    - `500 Internal Server Error`: If processing fails.

---

## 2. Get Top Customers
- **Endpoint**: `/api/customers/top`
- **Method**: `GET`
- **Query Parameters**:
    - `limit` (optional, integer): Number of top customers to return (default is 5).
- **Description**: Fetches the top customers by the number of tickets purchased.
- **Response**:
    ```json
    {
        "status": "success",
        "data": [
            {
                "customer_id": 1,
                "ticket_count": 10
            },
            {
                "customer_id": 2,
                "ticket_count": 8
            }
        ]
    }
    ```
- **Error Responses**:
    - `400 Bad Request`: If an invalid query parameter is provided.
    - `500 Internal Server Error`: If the operation fails.

---

## 3. Get Unused Barcodes
- **Endpoint**: `/api/barcodes/unused`
- **Method**: `GET`
- **Description**: Retrieves unused barcodes that are not yet associated with any order.
- **Response**:
    ```json
    {
        "status": "success",
        "data": {
            "count": 3,
            "barcodes": [
                {
                    "barcode": 54321,
                    "order_id": null
                },
                {
                    "barcode": 67890,
                    "order_id": null
                }
            ]
        }
    }
    ```
- **Error Responses**:
    - `500 Internal Server Error`: If the operation fails.

---

## 4. Get Customer Orders
- **Endpoint**: `/api/orders/<customer_id>`
- **Method**: `GET`
- **Description**: Fetches all orders for a specific customer.
- **Path Parameters**:
    - `customer_id` (integer): The ID of the customer whose orders are to be fetched.
- **Response**:
    ```json
    {
        "status": "success",
        "data": [
            {
                "order_id": 101,
                "barcodes": [12345, 67890]
            },
            {
                "order_id": 102,
                "barcodes": [54321]
            }
        ]
    }
    ```
- **Error Responses**:
    - `404 Not Found`: If no orders are found for the given customer.
    - `500 Internal Server Error`: If the operation fails.

---

## General Error Response Format
All error responses follow this standard format:
```json
{
    "status": "error",
    "message": "Error details here"
}
```

---

## Notes
- All endpoints return JSON responses.
- The API adheres to RESTful design principles for ease of integration.
- Authentication is currently not implemented but can be added later if required.
```
