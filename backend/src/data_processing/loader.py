import pandas as pd
from pathlib import Path
import logging
from .validator import orders_schema, barcodes_schema


class DataLoader:
    def __init__(self, input_dir: str = "data/input", logger=None):
        """Initialize DataLoader with input directory and logger.

        Args:
            input_dir (str): Path to input data directory
            logger (logging.Logger, optional): Logger instance
        """
        self.input_dir = Path(input_dir)
        self.logger = logger or logging.getLogger(__name__)
        self._barcodes_df = None  # Cache the loaded data

    def _check_duplicate_barcodes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Check and handle duplicate barcodes.

        Args:
            df (pd.DataFrame): DataFrame containing barcode data

        Returns:
            pd.DataFrame: DataFrame with duplicate barcodes removed
        """
        duplicates = df[df["barcode"].duplicated()]
        if not duplicates.empty:
            self.logger.warning(
                f"\nFound {len(duplicates)} duplicate barcodes:\n"
                f"{duplicates['barcode'].to_string()}"
            )
            df = df.drop_duplicates(subset=["barcode"], keep="first")
        return df

    def load_orders(self) -> pd.DataFrame:
        """Load and validate orders data.

        Returns:
            pd.DataFrame: Validated orders data

        Raises:
            FileNotFoundError: If orders.csv is not found
            ValidationError: If data doesn't match expected schema
        """
        try:
            df = pd.read_csv(self.input_dir / "orders.csv")
            return orders_schema.validate(df)
        except FileNotFoundError:
            self.logger.error(
                f"Orders file not found at {self.input_dir / 'orders.csv'}"
            )
            raise
        except Exception as e:
            self.logger.error(f"Error loading orders data: {str(e)}")
            raise

    def load_barcodes(self) -> pd.DataFrame:
        """Load and validate barcodes data.

        Returns:
            pd.DataFrame: Validated barcodes data with duplicates removed

        Raises:
            FileNotFoundError: If barcodes.csv is not found
            ValidationError: If data doesn't match expected schema
        """
        if self._barcodes_df is not None:
            return self._barcodes_df

        try:
            df = pd.read_csv(self.input_dir / "barcodes.csv")
            df = self._check_duplicate_barcodes(df)
            self._barcodes_df = barcodes_schema.validate(df)
            return self._barcodes_df
        except FileNotFoundError:
            self.logger.error(
                f"Barcodes file not found at {self.input_dir / 'barcodes.csv'}"
            )
            raise
        except Exception as e:
            self.logger.error(f"Error loading barcodes data: {str(e)}")
            raise
