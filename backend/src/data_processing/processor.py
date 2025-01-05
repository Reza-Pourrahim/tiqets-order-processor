import logging
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from app import db
from app.models.models import Barcode, Customer, Order

from .loader import DataLoader


class OrderProcessor:
    def __init__(self, logger: logging.Logger, output_dir: str = "data/output"):
        """Initialize OrderProcessor.

        Args:
            logger (logging.Logger): Logger instance
            output_dir (str): Directory for output files
        """
        self.loader = DataLoader(logger=logger)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger

    def process(self) -> pd.DataFrame:
        """Process orders and barcodes data into merged dataset.

        Returns:
            pd.DataFrame: Processed data with columns:
                - customer_id: Customer identifier
                - order_id: Order identifier
                - barcode: List of barcodes for the order

        Raises:
            FileNotFoundError: If input files not found
            ValidationError: If data validation fails
            Exception: For other processing errors
        """
        try:
            self.logger.info("Loading data files...")
            orders_df = self.loader.load_orders()
            barcodes_df = self.loader.load_barcodes()

            # Add validation
            if orders_df.empty or barcodes_df.empty:
                raise ValueError("Empty input data")

            valid_orders_df = self._validate_orders_barcodes(orders_df, barcodes_df)
            result = self._merge_orders_barcodes(valid_orders_df, barcodes_df)

            # Validate result
            if result.empty:
                raise ValueError("No valid orders found after processing")

            return result

        except FileNotFoundError as e:
            self.logger.error(f"Input file not found: {str(e)}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            raise

    def _validate_orders_barcodes(
        self, orders_df: pd.DataFrame, barcodes_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Validate all orders have associated barcodes.

        Args:
            orders_df (pd.DataFrame): Orders data
            barcodes_df (pd.DataFrame): Barcodes data

        Returns:
            pd.DataFrame: Valid orders data with invalid orders removed
        """
        # Retrieves the order_ids that have at least one barcode.
        orders_with_barcodes = barcodes_df["order_id"].unique()
        orders_without_barcodes = orders_df[
            ~orders_df["order_id"].isin(orders_with_barcodes)
        ]

        if not orders_without_barcodes.empty:
            self.logger.error(
                f"Found {len(orders_without_barcodes)} orders without barcodes: "
                f"{orders_without_barcodes['order_id'].tolist()}"
            )
            return orders_df[
                ~orders_df["order_id"].isin(orders_without_barcodes["order_id"])
            ]
        return orders_df

    def _merge_orders_barcodes(
        self, orders_df: pd.DataFrame, barcodes_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Merge orders with their barcodes.

        Args:
            orders_df (pd.DataFrame): Validated orders data
            barcodes_df (pd.DataFrame): Barcodes data

        Returns:
            pd.DataFrame: Merged data sorted by customer_id and order_id
        """
        try:
            barcodes_grouped = (
                barcodes_df.groupby("order_id")["barcode"].agg(list).reset_index()
            )
            result = orders_df.merge(barcodes_grouped, on="order_id", how="inner")
            return result.sort_values(["customer_id", "order_id"])
        except Exception as e:
            self.logger.error(f"Error merging orders and barcodes: {str(e)}")
            raise

    def get_top_customers(
        self, df: pd.DataFrame, limit: int = 5
    ) -> List[Tuple[int, int]]:
        """Get customers who purchased most tickets.

        Args:
            df (pd.DataFrame): Processed orders data
            limit (int): Number of top customers to return

        Returns:
            List[Tuple[int, int]]: List of (customer_id, ticket_count) tuples
        """
        try:
            self.logger.info(f"Calculating top {limit} customers...")
            customer_tickets = (
                df.explode("barcode").groupby("customer_id").size().nlargest(limit)
            )
            return list(customer_tickets.items())
        except Exception as e:
            self.logger.error(f"Error calculating top customers: {str(e)}")
            raise

    def get_unused_barcodes(self, df: pd.DataFrame) -> Tuple[int, pd.DataFrame]:
        """Get count and details of unused barcodes.

        Args:
            df (pd.DataFrame): Processed data

        Returns:
            Tuple[int, pd.DataFrame]: Count of unused barcodes and their details

        Raises:
            Exception: If error occurs while processing barcodes
        """
        try:
            barcodes_df = self.loader.load_barcodes()
            unused_barcodes = barcodes_df[barcodes_df["order_id"].isna()]
            return unused_barcodes.shape[0], unused_barcodes
        except Exception as e:
            self.logger.error(f"Error processing unused barcodes: {str(e)}")
            raise

    def save_results(self, df: pd.DataFrame) -> None:
        """Save processed orders to CSV.

        Args:
            df (pd.DataFrame): Processed data to save

        Raises:
            Exception: If saving fails
        """
        try:
            self.logger.info("Saving processed data...")
            output_df = df[["customer_id", "order_id", "barcode"]]
            output_path = self.output_dir / "processed_orders.csv"
            output_df.to_csv(output_path, index=False)
            self.logger.info(f"Results saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            raise

    def save_to_database(self, result_df: pd.DataFrame) -> None:
        try:
            self.logger.info("Saving data to database...")
            for _, row in result_df.iterrows():
                # Check if customer exists
                customer = Customer.query.get(row["customer_id"])
                if not customer:
                    customer = Customer(id=row["customer_id"])
                    db.session.add(customer)

                # Create order
                order = Order(customer_id=customer.id)
                db.session.add(order)

                # Create barcodes - check for existing ones
                for barcode_value in row["barcode"]:
                    # Check if barcode already exists
                    existing_barcode = Barcode.query.filter_by(
                        barcode_value=str(barcode_value)
                    ).first()

                    if not existing_barcode:
                        barcode = Barcode(
                            barcode_value=str(barcode_value), order_id=order.id
                        )
                        db.session.add(barcode)
                    else:
                        self.logger.warning(
                            f"Barcode {barcode_value} already exists, skipping..."
                        )

                db.session.commit()

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error saving to database: {str(e)}")
            raise
