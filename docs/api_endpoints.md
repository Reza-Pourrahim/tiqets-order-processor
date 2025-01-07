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
- **Description**: Processes the order and barcode data, saves the results to the database, and returns processed orders and analytics.
- **Response**:
    ```json
    {
        "status": "success",
        "data": {
            "orders": [
                {
                    "customer_id": 4,
                    "order_id": 193,
                    "barcodes": [11111111297, 11111111380, 11111111614]
                }
            ],
            "analytics": {
                "top_customers": [
                    {
                        "customer_id": 10,
                        "ticket_count": 23
                    }
                ],
                "unused_barcodes": {
                    "count": 98,
                    "barcodes": [
                        {
                            "barcode": 11111111635,
                            "order_id": None
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
                "customer_id": 10,
                "ticket_count": 23
            },
            {
                "customer_id": 56,
                "ticket_count": 20
            }
        ]
    }
    ```
- **Error Responses**:
    - `400 Bad Request`: Invalid query parameter.
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
            "count": 98,
            "barcodes": [
                {
                    "barcode": 11111111635,
                    "order_id": None
                },
                {
                    "barcode": 11111111636,
                    "order_id": None
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
                "customer_id": 10,
                "order_id": 1,
                "barcodes": [11111111111, 11111111318, 11111111428]
            },
            {
                "customer_id": 10,
                "order_id": 139,
                "barcodes": [11111111248, 11111111565]
            }
        ]
    }
    ```
- **Error Responses**:
    - `404 Not Found`: No orders found for the customer.
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

