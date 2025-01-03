import pandera as pa

# Schema for validating orders data
orders_schema = pa.DataFrameSchema(
    {
        "order_id": pa.Column(
            int, unique=True, description="Unique identifier for each order"
        ),
        "customer_id": pa.Column(
            int, description="Customer identifier - can have multiple orders"
        ),
    }
)

# Schema for validating barcodes data
barcodes_schema = pa.DataFrameSchema(
    {
        "barcode": pa.Column(
            int, unique=True, description="Unique identifier for each ticket"
        ),
        "order_id": pa.Column(
            float,
            nullable=True,
            description="Order ID if barcode is sold, null if unused",
        ),
    }
)
