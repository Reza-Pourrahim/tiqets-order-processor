from pathlib import Path

import pandas as pd
import pytest
from src.data_processing.processor import OrderProcessor
from src.utils.logger import setup_logger


def test_process_valid_data(app, sample_data):
    """Test processing of valid data."""
    with app.app_context():
        processor = OrderProcessor(
            logger=setup_logger(),
            input_dir=str(sample_data["input_dir"]),
            output_dir=str(sample_data["output_dir"]),
        )

        # Ensure we're using test data
        processor.loader.input_dir = sample_data["input_dir"]

        result = processor.process()

        assert not result.empty
        assert "customer_id" in result.columns
        assert "order_id" in result.columns
        assert "barcode" in result.columns

        # Only expect orders with barcodes
        expected_orders = (
            len(sample_data["orders"]) - 1
        )  # Exclude order without barcodes
        assert len(result) == expected_orders

        # Verify order details
        assert set(result["customer_id"].unique()) == {101, 102}
        assert set(result["order_id"].unique()) == {1, 2}  # Order 3 has no barcodes
        assert all(isinstance(barcodes, list) for barcodes in result["barcode"])


def test_get_top_customers(app, sample_data):
    """Test top customers calculation."""
    with app.app_context():
        processor = OrderProcessor(
            logger=setup_logger(),
            input_dir=str(sample_data["input_dir"]),
            output_dir=str(sample_data["output_dir"]),
        )
        result_df = processor.process()
        top_customers = processor.get_top_customers(result_df, limit=2)

        assert len(top_customers) <= 2
        assert all(
            isinstance(customer_id, int) and isinstance(count, int)
            for customer_id, count in top_customers
        )


def test_get_unused_barcodes(app, sample_data):
    """Test unused barcodes calculation."""
    with app.app_context():
        processor = OrderProcessor(
            setup_logger(),
            input_dir=str(sample_data["input_dir"]),
            output_dir=str(sample_data["output_dir"]),
        )

        # Ensure we're using test data
        processor.loader.input_dir = sample_data["input_dir"]

        # Use the sample data we created
        result_df = processor.process()
        count, unused_df = processor.get_unused_barcodes(result_df)

        assert count == 1  # One barcode has order_id=None
        assert not unused_df.empty
        assert "barcode" in unused_df.columns
        assert unused_df["order_id"].isnull().all()


def test_save_results(app, sample_data):
    """Test saving results to CSV."""
    with app.app_context():
        output_dir = str(sample_data["output_dir"])
        processor = OrderProcessor(
            setup_logger(),
            input_dir=str(sample_data["input_dir"]),
            output_dir=output_dir,
        )
        result_df = processor.process()
        processor.save_results(result_df)

        output_file = Path(output_dir) / "processed_orders.csv"
        assert output_file.exists()

        # Verify saved data
        saved_data = pd.read_csv(output_file)
        assert not saved_data.empty
        assert all(
            col in saved_data.columns for col in ["customer_id", "order_id", "barcode"]
        )
