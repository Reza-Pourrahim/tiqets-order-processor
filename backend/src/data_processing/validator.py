import pandera as pa

# Schema configuration notes:
# - strict=True: Ensures DataFrame has exactly these columns, no extra columns allowed
# - coerce=True: Automatically converts data types (e.g., string "123" to integer 123)

# Schema for validating orders data
orders_schema = pa.DataFrameSchema(
    {
        "order_id": pa.Column(
            int, 
            unique=True,
            coerce=True,  # Convert to integer if needed
            description="Unique identifier for each order"
        ),
        "customer_id": pa.Column(
            int,
            coerce=True,  # Convert to integer if needed
            description="Customer identifier - can have multiple orders"
        )
    },
    strict=True  # Ensure no unexpected columns
)

# Schema for validating barcodes data
barcodes_schema = pa.DataFrameSchema(
    {
        "barcode": pa.Column(
            int,
            unique=True,
            coerce=True,  # Convert to integer if needed
            description="Unique identifier for each ticket"
        ),
        "order_id": pa.Column(
            float,
            nullable=True,
            coerce=True,  # Convert to float if needed
            description="Order ID if barcode is sold, null if unused"
        )
    },
    strict=True  # Ensure no unexpected columns
)