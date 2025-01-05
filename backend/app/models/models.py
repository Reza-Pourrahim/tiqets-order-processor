from datetime import datetime, timezone

from app import db


class Customer(db.Model):
    """Customer model representing ticket buyers."""

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    # Relationships
    orders = db.relationship("Order", back_populates="customer", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Order(db.Model):
    """Order model for tracking ticket purchases."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    # Relationships
    customer = db.relationship("Customer", back_populates="orders")
    barcodes = db.relationship("Barcode", back_populates="order", lazy="dynamic")

    # Indexes
    __table_args__ = (db.Index("idx_customer_id", customer_id),)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "barcodes": [barcode.to_dict() for barcode in self.barcodes],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Barcode(db.Model):
    """Barcode model for tracking individual tickets."""

    __tablename__ = "barcodes"

    id = db.Column(db.Integer, primary_key=True)
    barcode_value = db.Column(db.String(255), unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=True)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    # Relationships
    order = db.relationship("Order", back_populates="barcodes")

    # Indexes
    __table_args__ = (
        db.Index("idx_order_id", order_id),
        db.Index("idx_barcode_value", barcode_value, unique=True),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "barcode_value": self.barcode_value,
            "order_id": self.order_id,
            "is_used": self.is_used,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
