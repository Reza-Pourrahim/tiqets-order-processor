from marshmallow import Schema, fields, validate


class BarcodeSchema(Schema):
    """Schema for barcode data"""

    barcode = fields.Int(required=True)
    order_id = fields.Int(allow_none=True)


class OrderSchema(Schema):
    """Schema for validating order data"""

    customer_id = fields.Int(required=True)
    order_id = fields.Int(required=True)
    barcodes = fields.List(fields.Int())


class CustomerOrderQuerySchema(Schema):
    """Schema for validating customer order query parameters"""

    limit = fields.Int(validate=validate.Range(min=1, max=100), load_default=5)


class TopCustomerSchema(Schema):
    """Schema for top customer response"""

    customer_id = fields.Int()
    ticket_count = fields.Int()


class UnusedBarcodeSchema(Schema):
    """Schema for unused barcode response"""

    count = fields.Int()
    barcodes = fields.List(fields.Nested(BarcodeSchema))
