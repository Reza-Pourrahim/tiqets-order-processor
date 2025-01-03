import pandas as pd
from pathlib import Path
from typing import Tuple, List
import logging
from .loader import DataLoader


class OrderProcessor:
    def __init__(self, logger: logging.Logger, output_dir: str = "data/output"):
        self.loader = DataLoader()
        self.output_dir = Path(output_dir)
        # create output directory and any missing parent dirs
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger

    def process(self) -> pd.DataFrame:
        """Process orders and barcodes data

        Returns:
            pd.DataFrame: Processed data with columns [customer_id, order_id, barcode]
            where barcode is a list of barcodes for each order

        Raises:
            FileNotFoundError: If input CSV files are not found
            ValidationError: If data validation fails
        """
        try:
            self.logger.info("Loading data files...")
            orders_df = self.loader.load_orders()
            barcodes_df = self.loader.load_barcodes()

            # Validate orders have barcodes
            self._validate_orders_barcodes(orders_df, barcodes_df)

            # Process and merge data
            result = self._merge_orders_barcodes(orders_df, barcodes_df)

            return result

        except FileNotFoundError as e:
            self.logger.error(f"Input file not found: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            raise

    def _validate_orders_barcodes(
        self, orders_df: pd.DataFrame, barcodes_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Validate that all orders have associated barcodes"""
        orders_with_barcodes = barcodes_df.groupby("order_id").size().index
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
        """Merge orders with their barcodes"""
        # Group barcodes as lists per order
        barcodes_grouped = (
            barcodes_df.groupby("order_id")["barcode"].agg(list).reset_index()
        )

        # Merge and sort results
        result = orders_df.merge(barcodes_grouped, on="order_id", how="inner")
        return result.sort_values(["customer_id", "order_id"])

    def get_top_customers(
        self, df: pd.DataFrame, limit: int = 5
    ) -> List[Tuple[int, int]]:
        """Get top customers by number of tickets purchased"""
        self.logger.info(f"Calculating top {limit} customers...")
        customer_tickets = (
            df.explode("barcode").groupby("customer_id").size().nlargest(limit)
        )

        return list(customer_tickets.items())

    def get_unused_barcodes(self, df: pd.DataFrame) -> int:
        """Calculate number of unused barcodes"""
        barcodes_df = self.loader.load_barcodes()
        return barcodes_df["order_id"].isna().sum()

    def save_results(self, df: pd.DataFrame) -> None:
        """Save processed orders to CSV"""
        self.logger.info("Saving processed data...")

        output_df = df[["customer_id", "order_id", "barcode"]]
        output_path = self.output_dir / "processed_orders.csv"
        output_df.to_csv(output_path, index=False)

        self.logger.info(f"Results saved to {output_path}")
