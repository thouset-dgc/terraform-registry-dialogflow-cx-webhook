import logging
import os

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler


def get_logger(name: str = "default_logger"):
    """
    Sets up and returns a logger configured to work seamlessly for both
    local and cloud environments by checking environment variables.

    Args:
        name (str): The name of the logger (defaults to 'default_logger').

    Returns:
        logging.Logger: A pre-configured logger.
    """
    # Initialize the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if the logger is reused
    if not logger.handlers:
        # Check if running in Cloud Run by looking for K_SERVICE
        is_cloud_run = "K_SERVICE" in os.environ

        if is_cloud_run:
            # Use Cloud Logging in Cloud Run
            client = google.cloud.logging.Client()
            cloud_handler = CloudLoggingHandler(client)
            logger.addHandler(cloud_handler)
        else:
            # Add a StreamHandler for local testing
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter("[%(name)s] [%(levelname)s] %(message)s")
            )
            logger.addHandler(console_handler)

    return logger
