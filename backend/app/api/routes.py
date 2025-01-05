from functools import lru_cache
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, current_app, jsonify, request
from src.data_processing.processor import OrderProcessor
from src.utils.logger import setup_logger

bp = Blueprint("api", __name__)
logger = setup_logger()


def error_response(message: str, status_code: int) -> Tuple[Dict[str, Any], int]:
    """Create a standardized error response.

    Args:
        message (str): Error message
        status_code (int): HTTP status code

    Returns:
        Tuple[Dict[str, Any], int]: Error response and status code
    """
    return ({"status": "error", "message": message}, status_code)


# Add lru_cache(Least Recently Used Cache) to cache processed data
@lru_cache(maxsize=1)
def get_processed_data():
    """Cache and return processed data.

    Returns:
        pd.DataFrame: Processed order data
    """
    processor = OrderProcessor(logger)
    return processor.process()


@bp.route("/process", methods=["GET"])
def process_orders():
    """Process order and barcode data and return comprehensive results.

    Returns:
        JSON response containing:
        - Processed orders
        - Top customer analytics
        - Unused barcode information

    Response format:
    {
        "status": "success",
        "data": {
            "orders": [...],
            "analytics": {
                "top_customers": [...],
                "unused_barcodes": {
                    "count": int,
                    "details": [...]
                }
            }
        }
    }

    Error Responses:
        500: Internal Server Error - Processing failed
    """
    try:
        result_df = get_processed_data()

        # Get analytics
        processor = OrderProcessor(logger)
        top_customers = processor.get_top_customers(result_df)
        unused_count, unused_barcodes_df = processor.get_unused_barcodes(result_df)

        # Save both to CSV and database
        processor.save_results(result_df)
        processor.save_to_database(result_df)

        response = {
            "status": "success",
            "data": {
                "orders": result_df.to_dict(orient="records"),
                "analytics": {
                    "top_customers": [
                        {"customer_id": int(cust_id), "ticket_count": int(count)}
                        for cust_id, count in top_customers
                    ],
                    "unused_barcodes": {
                        "count": int(unused_count),
                        "details": unused_barcodes_df.to_dict(orient="records"),
                    },
                },
            },
        }

        return jsonify(response), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error processing orders: {str(e)}")
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


@bp.route("/customers/top", methods=["GET"])
def get_top_customers():
    """Get top customers by ticket count.

    Query Parameters:
        limit (int, optional): Number of top customers to return. Default is 5.

    Returns:
        JSON response containing list of top customers with their ticket counts.

    Response format:
    {
        "status": "success",
        "data": [
            {
                "customer_id": int,
                "ticket_count": int
            },
            ...
        ]
    }

    Error Responses:
        400: Bad Request - Invalid limit parameter
        500: Internal Server Error - Processing failed
    """
    try:
        limit = request.args.get("limit", default=5, type=int)
        if limit <= 0:
            return error_response(
                "Limit must be a positive integer", HTTPStatus.BAD_REQUEST
            )

        result_df = get_processed_data()
        processor = OrderProcessor(logger)
        top_customers = processor.get_top_customers(result_df, limit=limit)

        response = {
            "status": "success",
            "data": [
                {"customer_id": int(cust_id), "ticket_count": int(count)}
                for cust_id, count in top_customers
            ],
        }

        return jsonify(response), HTTPStatus.OK

    except ValueError as ve:
        return error_response(
            f"Invalid limit parameter: {str(ve)}", HTTPStatus.BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error getting top customers: {str(e)}")
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


@bp.route("/barcodes/unused", methods=["GET"])
def get_unused_barcodes():
    """Get information about unused barcodes in the system.

    Returns:
        JSON response containing:
        - Count of unused barcodes
        - Details of each unused barcode

    Response format:
    {
        "status": "success",
        "data": {
            "count": int,
            "barcodes": [
                {
                    "barcode": str,
                    "order_id": null
                },
                ...
            ]
        }
    }

    Error Responses:
        500: Internal Server Error - Processing failed
    """
    try:
        result_df = get_processed_data()
        processor = OrderProcessor(logger)
        unused_count, unused_barcodes_df = processor.get_unused_barcodes(result_df)

        response = {
            "status": "success",
            "data": {
                "count": int(unused_count),
                "barcodes": unused_barcodes_df.to_dict(orient="records"),
            },
        }

        return jsonify(response), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error getting unused barcodes: {str(e)}")
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


@bp.route("/orders/<int:customer_id>", methods=["GET"])
def get_customer_orders(customer_id):
    """Get all orders for a specific customer.

    Args:
        customer_id (int): ID of the customer

    Returns:
        JSON response containing all orders for the specified customer.

    Response format:
    {
        "status": "success",
        "data": [
            {
                "order_id": int,
                "barcode": list,
                ...
            },
            ...
        ]
    }

    Error Responses:
        404: Not Found - Customer has no orders
        500: Internal Server Error - Processing failed
    """
    try:
        result_df = get_processed_data()
        customer_orders = result_df[result_df["customer_id"] == customer_id]

        if customer_orders.empty:
            return error_response(
                f"No orders found for customer {customer_id}", HTTPStatus.NOT_FOUND
            )

        return (
            jsonify(
                {"status": "success", "data": customer_orders.to_dict(orient="records")}
            ),
            HTTPStatus.OK,
        )

    except Exception as e:
        logger.error(f"Error getting customer orders: {str(e)}")
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
