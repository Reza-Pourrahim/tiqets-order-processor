import os
import tempfile
from pathlib import Path

import pandas as pd
import pytest
from app import create_app, db
from app.models.models import Barcode, Customer, Order
from sqlalchemy import text


@pytest.fixture(scope="function")
def app(tmp_path):
    """Create and configure a test Flask application."""
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent.parent

    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = "test-secret-key"

        # Use temporary directories for test data
        INPUT_DIR = tmp_path / "input"
        OUTPUT_DIR = tmp_path / "output"

    # Create directories
    TestConfig.INPUT_DIR.mkdir(parents=True)
    TestConfig.OUTPUT_DIR.mkdir(parents=True)

    app = create_app(TestConfig)

    with app.app_context():
        # Enable foreign key support
        with db.engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON"))
            conn.commit()

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def sample_data():
    """Create temporary input and output directories for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = Path(temp_dir) / "input"
        output_dir = Path(temp_dir) / "output"
        input_dir.mkdir(parents=True)
        output_dir.mkdir(parents=True)

        # Create test data
        orders_data = pd.DataFrame(
            {"order_id": [1, 2, 3], "customer_id": [101, 102, 101]}
        )

        # Order 3 has no barcodes (this is intentional)
        barcodes_data = pd.DataFrame(
            {"barcode": [1001, 1002, 1003, 1004], "order_id": [1.0, 1.0, 2.0, None]}
        )

        # Save test CSV files
        orders_data.to_csv(input_dir / "orders.csv", index=False)
        barcodes_data.to_csv(input_dir / "barcodes.csv", index=False)

        yield {
            "orders": orders_data,
            "barcodes": barcodes_data,
            "input_dir": input_dir,
            "output_dir": output_dir,
        }


@pytest.fixture
def db_sample_data(app):
    """Create sample database records."""
    with app.app_context():
        db.session.begin_nested()  # Create a savepoint

        try:
            # Create customers
            customer1 = Customer(id=101)
            customer2 = Customer(id=102)
            db.session.add_all([customer1, customer2])
            db.session.flush()

            # Create orders
            order1 = Order(id=1, customer_id=101)
            order2 = Order(id=2, customer_id=102)
            db.session.add_all([order1, order2])
            db.session.flush()

            # Create barcodes
            barcode1 = Barcode(barcode_value="1001", order_id=1)
            barcode2 = Barcode(barcode_value="1002", order_id=1)
            barcode3 = Barcode(barcode_value="1003", order_id=2)
            db.session.add_all([barcode1, barcode2, barcode3])

            db.session.commit()

            return {
                "customers": [customer1, customer2],
                "orders": [order1, order2],
                "barcodes": [barcode1, barcode2, barcode3],
            }

        except Exception as e:
            db.session.rollback()
            raise e


@pytest.fixture
def setup_test_data(app):
    """Helper fixture to set up test data files."""

    def _setup(orders_data=None, barcodes_data=None):
        input_dir = app.config["INPUT_DIR"]
        output_dir = app.config["OUTPUT_DIR"]

        # Use default test data if none provided
        if orders_data is None:
            orders_data = pd.DataFrame({"order_id": [1, 2], "customer_id": [101, 102]})
        if barcodes_data is None:
            barcodes_data = pd.DataFrame(
                {"barcode": [1001, 1002, 1003], "order_id": [1.0, 1.0, 2.0]}
            )

        # Save test data to temporary directory
        orders_data.to_csv(input_dir / "orders.csv", index=False)
        barcodes_data.to_csv(input_dir / "barcodes.csv", index=False)

        return {"input_dir": input_dir, "output_dir": output_dir}

    return _setup
