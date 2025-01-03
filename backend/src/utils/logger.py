import logging
import sys
from pathlib import Path


def setup_logger(log_dir: str = "logs") -> logging.Logger:
    """Configure logging to both file and stderr"""
    # create log directory
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # create logger
    logger = logging.getLogger("tiqets_processor")
    logger.setLevel(logging.INFO)

    # Format for our log messages
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Log to file
    file_handler = logging.FileHandler(f"{log_dir}/processor.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log to stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    return logger
