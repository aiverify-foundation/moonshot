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
    log_extension = ".log"

    # Read environment variable
    log_filename = os.getenv("MS_LOG_NAME", "moonshot").lower()
    log_level = os.getenv("MS_LOG_LEVEL", "INFO").upper()
    log_write_to_file = os.getenv("MS_LOG_TO_FILE", "false").lower() == "true"

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s][%(filename)s::%(funcName)s(%(lineno)d)] %(message)s"
    )

    # Check name is valid
    if not name or not isinstance(name, str) or name is None:
        name = Path(__file__).stem

    # Check log level is valid
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
    if log_level not in valid_log_levels:
        log_level = "INFO"

    # Check log filename is valid
    if not log_filename or not isinstance(log_filename, str) or log_filename is None:
        log_filename = "moonshot"

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    # Check if there is already a stream handler
    if not any(
        isinstance(handler, logging.StreamHandler) for handler in logger.handlers
    ):
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Create a file handler if required
    if log_write_to_file and not any(
        isinstance(handler, logging.FileHandler) for handler in logger.handlers
    ):
        file_path = Path(".").joinpath(log_filename).with_suffix(log_extension)
        file_handler = logging.FileHandler(
            str(file_path)
        )  # Convert Path object to string
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
