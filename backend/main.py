import signal
import sys

from src.data_processing.processor import OrderProcessor
from src.utils.logger import setup_logger


def signal_handler(sig, frame):
    print("\nProcessing interrupted by user")
    sys.exit(0)


def main():
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)

    # setup logger
    logger = setup_logger()
    logger.info("Starting order processing...")

    try:
        # initialize processor
        processor = OrderProcessor(logger)

        # process data
        result_df = processor.process()

        # get top customers
        top_customers = processor.get_top_customers(result_df)
        print("\nTop 5 customers by number of tickets:")
        for customer_id, ticket_count in top_customers:
            print(f"Customer {customer_id}: {ticket_count}")

        # get unused barcodes count
        unused_count, _ = processor.get_unused_barcodes(result_df)
        print(f"\nUnused barcodes: {unused_count}")

        # save results
        processor.save_results(result_df)
        logger.info("Processing completed successfully")

    except Exception as e:
        logger.error(f"Error processing orders: {str(e)}")
        raise


if __name__ == "__main__":
    main()
