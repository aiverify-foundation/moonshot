import logging
import os
from pathlib import Path


def configure_logger(name: str):
    """
    Configures and returns a logger with a specified name.

    This function creates a logger and sets its level to INFO. It also creates a console handler,
    sets its level to INFO, and assigns a specific formatter to it. The formatter includes the
    timestamp, log level, filename, function name, line number, and the log message. Finally, the
    console handler is added to the logger.

    Args:
        name (str): The name of the logger to be created and configured.

    Returns:
        logging.Logger: The configured logger with the specified name.
    """
    # Read environment variable
    log_filename = os.getenv("MS_LOG_NAME", "moonshot").lower()
    log_level = os.getenv("MS_LOG_LEVEL", "INFO").upper()
    log_write_to_file = os.getenv("MS_LOG_TO_FILE", "false").lower() == "true"

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s][%(filename)s::%(funcName)s(%(lineno)d)] %(message)s"
    )

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create a file handler if required
    if log_write_to_file:
        file_path = Path(".") / log_filename  # Use Path to create the file path
        file_handler = logging.FileHandler(
            str(file_path)
        )  # Convert Path object to string
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
