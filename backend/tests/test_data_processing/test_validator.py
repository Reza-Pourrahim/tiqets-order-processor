import pandas as pd
import pytest
from src.data_processing.validator import barcodes_schema, orders_schema


def test_valid_orders_data():
    """Test validation of correct orders data."""
    valid_data = pd.DataFrame({"order_id": [1, 2, 3], "customer_id": [101, 102, 103]})

    validated_df = orders_schema.validate(valid_data)
    assert validated_df is not None
    assert len(validated_df) == 3
    assert list(validated_df.columns) == ["order_id", "customer_id"]


def test_invalid_orders_data():
    """Test validation fails with incorrect orders data."""
    # Missing required column
    invalid_data = pd.DataFrame({"order_id": [1, 2, 3]})

    with pytest.raises(Exception):
        orders_schema.validate(invalid_data)

    # Wrong data type
    invalid_data = pd.DataFrame(
        {"order_id": ["a", "b", "c"], "customer_id": [101, 102, 103]}
    )

    with pytest.raises(Exception):
        orders_schema.validate(invalid_data)


def test_valid_barcodes_data():
    """Test validation of correct barcodes data."""
    valid_data = pd.DataFrame(
        {"barcode": [1001, 1002, 1003], "order_id": [1.0, 2.0, None]}
    )

    validated_df = barcodes_schema.validate(valid_data)
    assert validated_df is not None
    assert len(validated_df) == 3
    assert list(validated_df.columns) == ["barcode", "order_id"]


def test_invalid_barcodes_data():
    """Test validation fails with incorrect barcodes data."""
    # Missing required column
    invalid_data = pd.DataFrame({"order_id": [1.0, 2.0, None]})

    with pytest.raises(Exception):
        barcodes_schema.validate(invalid_data)

    # Wrong data type
    invalid_data = pd.DataFrame(
        {"barcode": ["abc", "def", "ghi"], "order_id": [1.0, 2.0, None]}
    )

    with pytest.raises(Exception):
        barcodes_schema.validate(invalid_data)


def test_duplicate_barcodes():
    """Test validation fails with duplicate barcodes."""
    invalid_data = pd.DataFrame(
        {
            "barcode": [1001, 1001, 1002],  # Duplicate barcode
            "order_id": [1.0, 1.0, 2.0],
        }
    )

    with pytest.raises(Exception):
        barcodes_schema.validate(invalid_data)
