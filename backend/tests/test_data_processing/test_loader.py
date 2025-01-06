import tempfile
from pathlib import Path

import pandas as pd
import pytest
from src.data_processing.loader import DataLoader


@pytest.fixture
def test_data_dir():
    """Create a temporary directory with sample CSV files."""
    temp_dir = tempfile.mkdtemp()
    input_dir = Path(temp_dir) / "input"
    input_dir.mkdir(parents=True)

    # Create test data
    orders_df = pd.DataFrame({"order_id": [1, 2, 3], "customer_id": [101, 102, 101]})
    orders_df.to_csv(input_dir / "orders.csv", index=False)

    barcodes_df = pd.DataFrame(
        {"barcode": [1001, 1002, 1003, 1004], "order_id": [1.0, 1.0, 2.0, None]}
    )
    barcodes_df.to_csv(input_dir / "barcodes.csv", index=False)

    yield input_dir

    # Cleanup
    import shutil

    shutil.rmtree(temp_dir)


def test_load_orders(test_data_dir):
    """Test loading orders data."""
    loader = DataLoader(str(test_data_dir))
    orders_df = loader.load_orders()

    assert not orders_df.empty
    assert "order_id" in orders_df.columns
    assert "customer_id" in orders_df.columns
    assert len(orders_df) == 3


def test_load_barcodes(test_data_dir):
    """Test loading barcodes data."""
    loader = DataLoader(str(test_data_dir))
    barcodes_df = loader.load_barcodes()

    assert not barcodes_df.empty
    assert "barcode" in barcodes_df.columns
    assert "order_id" in barcodes_df.columns
    assert len(barcodes_df) == 4


def test_missing_files():
    """Test handling of missing input files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        loader = DataLoader(temp_dir)

        with pytest.raises(FileNotFoundError):
            loader.load_orders()

        with pytest.raises(FileNotFoundError):
            loader.load_barcodes()


def test_duplicate_barcodes(test_data_dir):
    """Test handling of duplicate barcodes."""
    # Create data with duplicate barcodes
    barcodes_df = pd.DataFrame(
        {
            "barcode": [1001, 1001, 1002],  # Duplicate barcode
            "order_id": [1.0, 2.0, 3.0],
        }
    )
    barcodes_df.to_csv(test_data_dir / "barcodes.csv", index=False)

    loader = DataLoader(str(test_data_dir))
    result_df = loader.load_barcodes()

    # Should only keep first occurrence of duplicate
    assert len(result_df) == 2
    assert len(result_df[result_df["barcode"] == 1001]) == 1


def test_invalid_data(test_data_dir):
    """Test handling of invalid data in CSV files."""
    # Create invalid orders data
    invalid_orders = pd.DataFrame({"wrong_column": [1, 2, 3]})
    invalid_orders.to_csv(test_data_dir / "orders.csv", index=False)

    loader = DataLoader(str(test_data_dir))
    with pytest.raises(Exception):
        loader.load_orders()
