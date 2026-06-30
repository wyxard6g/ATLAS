"""
ATLAS Logging Module
"""

import logging
import sys


def setup_logger() -> logging.Logger:
    """
    Configure and return the main ATLAS logger.
    """

    logger = logging.getLogger("ATLAS")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


logger = setup_logger()