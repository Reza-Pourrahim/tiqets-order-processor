import json

import pandas as pd
import pytest
from app import db
from app.api.routes import get_processed_data
from app.models.models import Barcode, Customer, Order


def test_process_orders_endpoint(client, sample_data, setup_test_data):
    """Test the main processing endpoint."""
    # Set up test data files
    setup_test_data()

    # Clear cache
    get_processed_data.cache_clear()

    response = client.get("/api/process")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert "orders" in data["data"]
    assert "analytics" in data["data"]


def test_top_customers_endpoint(client, sample_data, setup_test_data):
    """Test the top customers endpoint."""
    # Set up test data files
    setup_test_data()

    # Clear cache
    get_processed_data.cache_clear()

    # Test default limit
    response = client.get("/api/customers/top")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["data"]) <= 5


def test_unused_barcodes_endpoint(client, sample_data, setup_test_data):
    """Test the unused barcodes endpoint."""
    # Set up test data files
    setup_test_data()

    # Clear cache
    get_processed_data.cache_clear()

    response = client.get("/api/barcodes/unused")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "count" in data["data"]
    assert "barcodes" in data["data"]


def test_customer_orders_endpoint(client, db_sample_data, app, setup_test_data):
    """Test the customer orders endpoint."""
    with app.app_context():
        # Set up test data files
        setup_test_data()

        # Clear cache
        get_processed_data.cache_clear()

        # Test existing customer
        response = client.get("/api/orders/101")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert len(data["data"]) > 0


@pytest.mark.parametrize(
    "endpoint",
    ["/api/process", "/api/customers/top", "/api/barcodes/unused", "/api/orders/101"],
)
def test_endpoint_response_structure(client, db_sample_data, setup_test_data, endpoint):
    """Test consistent response structure across endpoints."""
    # Set up test data files
    setup_test_data()

    # Clear cache
    get_processed_data.cache_clear()

    response = client.get(endpoint)
    assert response.status_code in [200, 404]
    data = json.loads(response.data)
    assert "status" in data
