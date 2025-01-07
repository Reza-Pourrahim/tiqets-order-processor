from functools import lru_cache
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, Tuple

from app.schemas.schemas import (
    CustomerOrderQuerySchema,
    OrderSchema,
    TopCustomerSchema,
    UnusedBarcodeSchema,
)
from flask import Blueprint, current_app, jsonify, request
from marshmallow import ValidationError
from src.data_processing.processor import OrderProcessor
from src.utils.logger import setup_logger

bp = Blueprint("api", __name__)
logger = setup_logger()

# Initialize schemas
order_schema = OrderSchema()
customer_query_schema = CustomerOrderQuerySchema()
top_customer_schema = TopCustomerSchema(many=True)
unused_barcode_schema = UnusedBarcodeSchema()


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
def get_processed_data(input_dir: str, output_dir: str):
    """Cache and return processed data.

    Args:
        input_dir (str): Input directory path
        output_dir (str): Output directory path

    Returns:
        pd.DataFrame: Processed order data
    """
    processor = OrderProcessor(
        logger=logger, input_dir=input_dir, output_dir=output_dir
    )

    # Set the input directory for the loader
    processor.loader.input_dir = Path(input_dir)

    return processor.process()


@bp.route("/", methods=["GET"])
def index():
    """Default route to verify the API is running."""
    return {"message": "Welcome to the Tiqets Order Processor API!"}, 200


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
        # Get paths from config
        input_dir = str(current_app.config["INPUT_DIR"])
        output_dir = str(current_app.config["OUTPUT_DIR"])

        # Use cached data processing
        result_df = get_processed_data(input_dir, output_dir)

        # Create processor for operations
        processor = OrderProcessor(
            logger=logger, input_dir=input_dir, output_dir=output_dir
        )

        # Save both to CSV and database
        processor.save_results(result_df)
        processor.save_to_database(result_df)

        # Get analytics
        top_customers = processor.get_top_customers(result_df)
        unused_count, unused_barcodes_df = processor.get_unused_barcodes(result_df)

        # Prepare response data
        response = {
            "status": "success",
            "data": {
                "orders": order_schema.dump(
                    [
                        {
                            "customer_id": int(row["customer_id"]),
                            "order_id": int(row["order_id"]),
                            "barcodes": [int(b) for b in row["barcode"]],
                        }
                        for _, row in result_df.iterrows()
                    ],
                    many=True,
                ),
                "analytics": {
                    "top_customers": top_customer_schema.dump(
                        [
                            {"customer_id": int(cust_id), "ticket_count": int(count)}
                            for cust_id, count in top_customers
                        ]
                    ),
                    "unused_barcodes": unused_barcode_schema.dump(
                        {
                            "count": int(unused_count),
                            "barcodes": [
                                {"barcode": int(row["barcode"]), "order_id": None}
                                for _, row in unused_barcodes_df.iterrows()
                            ],
                        }
                    ),
                },
            },
        }
        print(f"response process: {response}")

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
        params = customer_query_schema.load(request.args)
        input_dir = str(current_app.config["INPUT_DIR"])
        output_dir = str(current_app.config["OUTPUT_DIR"])

        result_df = get_processed_data(input_dir, output_dir)
        processor = OrderProcessor(
            logger=logger, input_dir=input_dir, output_dir=output_dir
        )
        top_customers = processor.get_top_customers(result_df, limit=params["limit"])

        result = top_customer_schema.dump(
            [
                {"customer_id": int(cust_id), "ticket_count": int(count)}
                for cust_id, count in top_customers
            ]
        )
        print(f"response get_top_customers: {result}")
        return jsonify({"status": "success", "data": result}), HTTPStatus.OK

    except ValidationError as err:
        return error_response(str(err.messages), HTTPStatus.BAD_REQUEST)
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
        input_dir = str(current_app.config["INPUT_DIR"])
        output_dir = str(current_app.config["OUTPUT_DIR"])

        result_df = get_processed_data(input_dir, output_dir)
        processor = OrderProcessor(logger)
        unused_count, unused_barcodes_df = processor.get_unused_barcodes(result_df)

        # Prepare data for schema
        data = {
            "count": int(unused_count),
            "barcodes": [
                {"barcode": int(row["barcode"]), "order_id": None}
                for _, row in unused_barcodes_df.iterrows()
            ],
        }

        # Validate and serialize with schema
        result = unused_barcode_schema.dump(data)
        print(f"response unused_barcode: {result}")

        return jsonify({"status": "success", "data": result}), HTTPStatus.OK

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
        input_dir = str(current_app.config["INPUT_DIR"])
        output_dir = str(current_app.config["OUTPUT_DIR"])

        result_df = get_processed_data(input_dir, output_dir)
        customer_orders = result_df[result_df["customer_id"] == customer_id]

        if customer_orders.empty:
            return error_response(
                f"No orders found for customer {customer_id}", HTTPStatus.NOT_FOUND
            )

        # Convert DataFrame to format matching schema
        orders_data = [
            {
                "customer_id": int(row["customer_id"]),
                "order_id": int(row["order_id"]),
                "barcodes": [int(b) for b in row["barcode"]],
            }
            for _, row in customer_orders.iterrows()
        ]

        # Validate and serialize with schema
        result = order_schema.dump(orders_data, many=True)

        return jsonify({"status": "success", "data": result}), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error getting customer orders: {str(e)}")
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
