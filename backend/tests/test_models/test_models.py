import pytest
from app import db
from app.models.models import Barcode, Customer, Order
from sqlalchemy.exc import IntegrityError


def test_customer_model(app):
    """Test Customer model operations."""
    with app.app_context():
        session = db.session  # Use the existing session from Flask-SQLAlchemy

        # Test creation
        customer = Customer(id=1)
        session.add(customer)
        session.commit()

        # Test retrieval
        retrieved = session.get(Customer, 1)
        assert retrieved is not None
        assert retrieved.id == 1

        # Test relationship with orders
        order = Order(customer_id=customer.id)
        session.add(order)
        session.commit()

        assert len(customer.orders.all()) == 1


def test_order_model(app):
    """Test Order model operations."""
    with app.app_context():
        # Test creation with valid customer
        customer = Customer(id=1)
        db.session.add(customer)
        db.session.commit()

        order = Order(customer_id=customer.id)
        db.session.add(order)
        db.session.commit()

        # Test foreign key constraint
        invalid_order = Order(customer_id=999)  # Non-existent customer
        db.session.add(invalid_order)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


def test_barcode_model(app):
    """Test Barcode model operations."""
    with app.app_context():
        # Setup
        customer = Customer(id=1)
        db.session.add(customer)
        order = Order(customer_id=customer.id)
        db.session.add(order)
        db.session.commit()

        # Test creation
        barcode = Barcode(barcode_value="12345", order_id=order.id)
        db.session.add(barcode)
        db.session.commit()

        # Test unique constraint
        duplicate = Barcode(barcode_value="12345", order_id=order.id)
        db.session.add(duplicate)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # Test nullable order_id (unused barcode)
        unused = Barcode(barcode_value="54321")
        db.session.add(unused)
        db.session.commit()

        # Verify unused barcode was saved
        assert unused.id is not None
