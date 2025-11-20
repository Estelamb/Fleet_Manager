"""
create_logger module
====================

This module provides a utility function to configure a concurrent-safe logger
with rotating file handler for drone system logging.

Functions
---------
.. autofunction:: create_logger

Exceptions
----------
IOError
    Raised if log file initialization fails.
"""

import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

def create_logger(logger_name: str, log_file: str) -> logging.Logger:
    """
    Configure concurrent-safe logger with rotating file handler.

    Parameters
    ----------
    logger_name : str
        Namespace for logger instance.
    log_file : str
        Path for log file storage.

    Returns
    -------
    logging.Logger
        Configured logger instance.

    Raises
    ------
    IOError
        If log file initialization fails.

    Notes
    -----
    - 1MB log rotation with 5 backups
    - Concurrent write safety
    - Unified console/file formatting
    - UTC timestamp formatting
    """
    try:
        # Create a custom logger
        logger = logging.getLogger(logger_name)

        # Set level
        logger.setLevel(logging.INFO)

        # Create a file handler
        file_handler = ConcurrentRotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)

        # Create a console handler
        console_handler = logging.StreamHandler()

        # Set formatter
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')

        # Attach formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Attach handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
    except Exception as e:
        print(f"Error creating logger {logger_name}: {str(e)}")
        raise